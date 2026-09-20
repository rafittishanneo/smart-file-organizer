from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, ttk


class FileOrganizerView(tk.Tk):
    BG = "#F4F7FB"
    CARD = "#FFFFFF"
    TEXT = "#172033"
    MUTED = "#637083"
    BORDER = "#DDE4EE"
    BLUE = "#2563EB"
    BLUE_DARK = "#1D4ED8"
    BLUE_LIGHT = "#EAF2FF"
    PURPLE = "#7C3AED"
    PURPLE_LIGHT = "#F1EBFF"
    GREEN = "#16A34A"
    GREEN_LIGHT = "#EAF8EF"
    HEADER = "#13233F"

    def __init__(self) -> None:
        super().__init__()
        self.title("Smart File Organizer")
        self.geometry("1120x700")
        self.minsize(920, 600)
        self.configure(bg=self.BG)

        self.folder_var = tk.StringVar()
        self.by_date_var = tk.BooleanVar(value=False)
        self.status_var = tk.StringVar(value="Ready — select a folder, then preview your files.")
        self.count_var = tk.StringVar(value="No folder selected")

        self._configure_styles()
        self._build_interface()

    def _configure_styles(self) -> None:
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("App.TFrame", background=self.BG)
        style.configure("Card.TFrame", background=self.CARD)
        style.configure("Header.TFrame", background=self.HEADER)

        style.configure("Title.TLabel", background=self.HEADER, foreground="#FFFFFF", font=("Segoe UI", 23, "bold"))
        style.configure("Subtitle.TLabel", background=self.HEADER, foreground="#C9D7F0", font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=self.CARD, foreground=self.TEXT, font=("Segoe UI", 11, "bold"))
        style.configure("Small.TLabel", background=self.CARD, foreground=self.MUTED, font=("Segoe UI", 9))
        style.configure("Status.TLabel", background=self.BG, foreground=self.MUTED, font=("Segoe UI", 9))

        style.configure(
            "Primary.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(18, 10),
            foreground="#FFFFFF",
            background=self.BLUE,
            borderwidth=0,
            focusthickness=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.BLUE_DARK), ("pressed", "#1E40AF"), ("disabled", "#A9C6FA")],
            foreground=[("disabled", "#F8FAFC")],
        )

        style.configure(
            "Purple.TButton",
            font=("Segoe UI Semibold", 10),
            padding=(16, 10),
            foreground="#FFFFFF",
            background=self.PURPLE,
            borderwidth=0,
            focusthickness=0,
        )
        style.map(
            "Purple.TButton",
            background=[("active", "#6D28D9"), ("pressed", "#5B21B6"), ("disabled", "#CDBBFA")],
            foreground=[("disabled", "#F8FAFC")],
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=(14, 10),
            foreground=self.TEXT,
            background="#F8FAFC",
            borderwidth=1,
            relief="solid",
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#EAF2FF"), ("pressed", "#D7E7FF"), ("disabled", "#F3F4F6")],
            foreground=[("disabled", "#9CA3AF")],
        )

        style.configure(
            "Modern.TEntry",
            font=("Segoe UI", 10),
            padding=(11, 10),
            fieldbackground="#FFFFFF",
            foreground=self.TEXT,
            bordercolor=self.BORDER,
            lightcolor=self.BORDER,
            darkcolor=self.BORDER,
        )
        style.configure(
            "Modern.TCheckbutton",
            background=self.CARD,
            foreground=self.TEXT,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Modern.Treeview",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground=self.TEXT,
            rowheight=38,
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.map(
            "Modern.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", self.TEXT)],
        )
        style.configure(
            "Modern.Treeview.Heading",
            background="#EEF4FF",
            foreground="#1E3A5F",
            font=("Segoe UI Semibold", 9),
            relief="flat",
            padding=(12, 11),
        )
        style.map("Modern.Treeview.Heading", background=[("active", "#DCEAFF")])

    def _build_interface(self) -> None:
        outer = ttk.Frame(self, style="App.TFrame", padding=(28, 24, 28, 18))
        outer.pack(fill="both", expand=True)

        header = ttk.Frame(outer, style="Header.TFrame", padding=(28, 24))
        header.pack(fill="x")
        ttk.Label(header, text="Smart File Organizer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Organize your files faster — preview, sort, detect duplicates, and undo safely.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(5, 0))

        body = ttk.Frame(outer, style="App.TFrame")
        body.pack(fill="both", expand=True, pady=(18, 0))
        body.columnconfigure(0, weight=1)
        body.rowconfigure(1, weight=1)

        selection_card = ttk.Frame(body, style="Card.TFrame", padding=22)
        selection_card.grid(row=0, column=0, sticky="ew")
        selection_card.columnconfigure(0, weight=1)

        title_row = ttk.Frame(selection_card, style="Card.TFrame")
        title_row.grid(row=0, column=0, sticky="ew")
        title_row.columnconfigure(0, weight=1)
        ttk.Label(title_row, text="Choose a folder", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(title_row, textvariable=self.count_var, style="Small.TLabel").grid(row=0, column=1, sticky="e")

        path_row = ttk.Frame(selection_card, style="Card.TFrame")
        path_row.grid(row=1, column=0, sticky="ew", pady=(11, 15))
        path_row.columnconfigure(0, weight=1)
        self.folder_entry = ttk.Entry(path_row, textvariable=self.folder_var, style="Modern.TEntry")
        self.folder_entry.grid(row=0, column=0, sticky="ew")
        self.browse_button = ttk.Button(path_row, text="Browse", style="Secondary.TButton")
        self.browse_button.grid(row=0, column=1, padx=(10, 0))

        actions_row = ttk.Frame(selection_card, style="Card.TFrame")
        actions_row.grid(row=2, column=0, sticky="ew")
        actions_row.columnconfigure(0, weight=1)
        self.date_checkbox = ttk.Checkbutton(
            actions_row,
            text="Create year-month subfolders",
            variable=self.by_date_var,
            style="Modern.TCheckbutton",
        )
        self.date_checkbox.grid(row=0, column=0, sticky="w")
        self.preview_button = ttk.Button(actions_row, text="Preview", style="Secondary.TButton")
        self.preview_button.grid(row=0, column=1, padx=(10, 10))
        self.organize_button = ttk.Button(
            actions_row,
            text="Organize files",
            style="Primary.TButton",
            width=18,
        )
        self.organize_button.grid(row=0, column=2, sticky="e")

        files_card = ttk.Frame(body, style="Card.TFrame", padding=22)
        files_card.grid(row=1, column=0, sticky="nsew", pady=(18, 0))
        files_card.rowconfigure(1, weight=1)
        files_card.columnconfigure(0, weight=1)

        heading_row = ttk.Frame(files_card, style="Card.TFrame")
        heading_row.grid(row=0, column=0, sticky="ew", pady=(0, 14))
        heading_row.columnconfigure(0, weight=1)
        ttk.Label(heading_row, text="File preview", style="Section.TLabel").grid(row=0, column=0, sticky="w")
        self.duplicates_button = ttk.Button(heading_row, text="Find duplicates", style="Secondary.TButton")
        self.duplicates_button.grid(row=0, column=1, padx=(0, 10))
        self.undo_button = ttk.Button(heading_row, text="Undo last operation", style="Purple.TButton")
        self.undo_button.grid(row=0, column=2)

        table_frame = ttk.Frame(files_card, style="Card.TFrame")
        table_frame.grid(row=1, column=0, sticky="nsew")
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        columns = ("name", "category", "destination", "size")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Modern.Treeview")
        settings = {
            "name": ("File name", 240),
            "category": ("Category", 135),
            "destination": ("Destination", 505),
            "size": ("Size", 95),
        }
        for key, (title, width) in settings.items():
            self.table.heading(key, text=title)
            self.table.column(key, width=width, minwidth=75, anchor="w")
        self.table.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.table.configure(yscrollcommand=scrollbar.set)

        footer = ttk.Frame(outer, style="App.TFrame")
        footer.pack(fill="x", pady=(14, 0))
        tk.Label(footer, text="●", bg=self.BG, fg=self.GREEN, font=("Segoe UI", 10)).pack(side="left")
        ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel").pack(side="left", padx=(6, 0))

    def choose_folder(self) -> str:
        return filedialog.askdirectory(title="Select a folder to organize")

    def clear_rows(self) -> None:
        for row_id in self.table.get_children():
            self.table.delete(row_id)

    def add_row(self, item: dict) -> None:
        self.table.insert(
            "",
            "end",
            values=(item["name"], item["category"], item["target"], self.format_size(item["size"])),
        )

    def update_file_count(self, count: int) -> None:
        word = "file" if count == 1 else "files"
        self.count_var.set(f"{count} {word} ready")

    @staticmethod
    def format_size(size: int) -> str:
        value = float(size)
        for unit in ("B", "KB", "MB", "GB"):
            if value < 1024 or unit == "GB":
                return f"{value:.1f} {unit}"
            value /= 1024
        return f"{value:.1f} GB"

    def set_controls_enabled(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        for control in (
            self.browse_button,
            self.preview_button,
            self.organize_button,
            self.duplicates_button,
            self.undo_button,
            self.date_checkbox,
        ):
            control.configure(state=state)
