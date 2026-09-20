from __future__ import annotations

import threading
from pathlib import Path
from tkinter import messagebox
from typing import Callable

from models.organizer_model import FileOrganizerModel
from views.organizer_view import FileOrganizerView


class FileOrganizerController:
    def __init__(self, model: FileOrganizerModel, view: FileOrganizerView) -> None:
        self.model = model
        self.view = view
        self.view.browse_button.configure(command=self.choose_folder)
        self.view.preview_button.configure(command=self.preview)
        self.view.organize_button.configure(command=self.organize)
        self.view.duplicates_button.configure(command=self.find_duplicates)
        self.view.undo_button.configure(command=self.undo)

    def choose_folder(self) -> None:
        folder = self.view.choose_folder()
        if folder:
            self.view.folder_var.set(folder)
            self.preview()

    def selected_directory(self) -> Path | None:
        raw_path = self.view.folder_var.get().strip()
        folder = Path(raw_path).expanduser()
        if not raw_path or not folder.is_dir():
            self.view.update_file_count(0)
            messagebox.showerror("Smart File Organizer", "Select a valid folder first.")
            return None
        return folder

    def preview(self) -> None:
        folder = self.selected_directory()
        if folder is None:
            return
        try:
            files = self.model.scan(folder, self.view.by_date_var.get())
            self.view.clear_rows()
            for file_info in files:
                self.view.add_row(file_info)

            self.view.update_file_count(len(files))
            self.view.status_var.set(
                f"Selected folder: {folder} | Preview ready: {len(files)} file(s) found. No files have been moved."
            )
        except (OSError, ValueError) as error:
            messagebox.showerror("Smart File Organizer", str(error))

    def organize(self) -> None:
        folder = self.selected_directory()
        if folder is None:
            return
        try:
            total = len(self.model.scan(folder, self.view.by_date_var.get()))
        except (OSError, ValueError) as error:
            messagebox.showerror("Smart File Organizer", str(error))
            return

        if total == 0:
            self.view.update_file_count(0)
            messagebox.showinfo("Smart File Organizer", "No files are available to organize in this folder.")
            return

        answer = messagebox.askyesno(
            "Confirm organization",
            f"Move {total} file(s) into category folders inside:\n\n{folder}\n\nYou can undo the latest completed operation.",
        )
        if answer:
            self.run_task(lambda: self._organize_task(folder), "Organizing files...")

    def _organize_task(self, folder: Path) -> None:
        records = self.model.organize(folder, self.view.by_date_var.get(), self.set_status)
        self.view.after(0, lambda: self.complete(f"Successfully organized {len(records)} file(s)."))

    def find_duplicates(self) -> None:
        folder = self.selected_directory()
        if folder is not None:
            self.run_task(lambda: self._duplicate_task(folder), "Checking files for exact duplicates...")

    def _duplicate_task(self, folder: Path) -> None:
        groups = self.model.find_duplicates(folder)
        self.view.after(0, lambda: self.show_duplicate_result(groups))

    def show_duplicate_result(self, groups: list[list[Path]]) -> None:
        self.view.set_controls_enabled(True)
        if not groups:
            self.view.status_var.set("Duplicate scan complete: no exact duplicates found.")
            messagebox.showinfo("Duplicate Detection", "No exact duplicate files were found.")
            return

        result = "\n\n".join(
            "Duplicate group:\n" + "\n".join(f"• {file.name}" for file in group)
            for group in groups
        )
        self.view.status_var.set(f"Duplicate scan complete: {len(groups)} duplicate group(s) found.")
        messagebox.showinfo("Duplicate Detection", result)

    def undo(self) -> None:
        if messagebox.askyesno("Undo", "Undo the most recent organization operation?"):
            self.run_task(self._undo_task, "Undoing latest operation...")

    def _undo_task(self) -> None:
        restored, errors = self.model.undo_last_operation(self.set_status)
        message = f"Restored {restored} file(s)."
        if errors:
            message += f" {len(errors)} file(s) could not be restored."
        self.view.after(0, lambda: self.complete(message))

    def run_task(self, task: Callable[[], None], starting_status: str) -> None:
        self.view.set_controls_enabled(False)
        self.view.status_var.set(starting_status)

        def worker() -> None:
            try:
                task()
            except Exception as error:
                self.view.after(0, lambda: self.fail(str(error)))

        threading.Thread(target=worker, daemon=True).start()

    def set_status(self, text: str) -> None:
        self.view.after(0, lambda: self.view.status_var.set(text))

    def complete(self, text: str) -> None:
        self.view.set_controls_enabled(True)
        self.preview()
        self.view.status_var.set(text)
        messagebox.showinfo("Smart File Organizer", text)

    def fail(self, error_text: str) -> None:
        self.view.set_controls_enabled(True)
        self.view.status_var.set("Operation failed.")
        messagebox.showerror("Smart File Organizer", error_text)
