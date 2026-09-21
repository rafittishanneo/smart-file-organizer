# Smart File Organizer

A Python desktop application that automatically organizes files into category folders. The application follows the Model-View-Controller (MVC) architecture and uses only Python's built-in standard library.

## Features

- Preview files and proposed destinations before moving anything
- Organize files by extension into category folders
- Automatically create required destination folders
- Optionally organize files into year-month subfolders
- Safely rename files with conflicting names instead of overwriting them
- Detect exact duplicate files using SHA-256 hashes
- Save activity logs
- Undo the most recent organization operation
- Simple Tkinter desktop graphical interface
- No external Python packages required

## File Categories

| Category | Supported extensions |
|---|---|
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`, `.tiff` |
| Documents | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.csv` |
| Videos | `.mp4`, `.mkv`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm` |
| Audio | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.m4a` |
| Archives | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` |
| Code | `.py`, `.js`, `.ts`, `.html`, `.css`, `.json`, `.xml`, `.java`, `.c`, `.cpp`, `.php`, `.sql` |
| Others | Any extension not listed above |

## Project Structure

```text
SmartFileOrganizer/
│
├── main.py
├── README.md
├── .gitignore
├── LICENSE
├── pyproject.toml
├── uv.lock
│
├── controllers/
│   ├── __init__.py
│   └── organizer_controller.py
│
├── models/
│   ├── __init__.py
│   └── organizer_model.py
│
└── views/
    ├── __init__.py
    └── organizer_view.py
```

## MVC Architecture

The application uses the **Model-View-Controller (MVC)** design pattern to keep the interface, application logic, and file-management operations separate.

| Component | File | Responsibilities |
|---|---|---|
| Application entry point | `main.py` | Starts the application and connects the Model, View, and Controller components |
| Model | `models/organizer_model.py` | Scans folders, identifies extensions, categorizes files, creates folders, moves files, detects duplicates, logs activity, and handles undo operations |
| View | `views/organizer_view.py` | Creates the Tkinter graphical user interface, including buttons, folder selector, preview table, and status messages |
| Controller | `controllers/organizer_controller.py` | Responds to user actions, connects the View and Model, and updates the interface with results or errors |

## Requirements

- Python 3.10 or later is recommended
- Tkinter, which is normally included with standard Python installations
- No external Python packages are required

## Installation

1. Clone the repository or download the project files.

```bash
git clone https://github.com/your-username/SmartFileOrganizer.git
```

2. Move into the project folder.

```bash
cd SmartFileOrganizer
```

3. Confirm that Python is installed.

```bash
python --version
```

On some systems, use:

```bash
python3 --version
```

## How to Run

Open a terminal in the project folder and run:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

For Windows PowerShell when using a virtual environment:

```powershell
.\.venv\Scripts\python.exe .\main.py
```

> Do not run `organizer_model.py`, `organizer_view.py`, or `organizer_controller.py` directly. Always start the application through `main.py`.

## How to Use

1. Run `main.py`.
2. Click **Browse** and select the folder you want to organize.
3. Click **Preview** to view the files and their proposed destinations. The preview does not move any files.
4. Optionally select **Create year-month subfolders**.
5. Click **Organize Files** and confirm the action.
6. Click **Find Duplicates** to search for files with identical SHA-256 hashes.
7. Click **Undo Last Operation** to restore files moved by the latest organization operation.

> **Important:** Test the application first with a copied test folder. Use extra care before organizing folders that contain important or irreplaceable files.

## Example Result

After organizing a Downloads folder, the result may look like this:

```text
Downloads/
│
├── Images/
│   └── photo.jpg
│
├── Documents/
│   ├── assignment.pdf
│   └── data.xlsx
│
├── Audio/
│   └── lecture.mp3
│
├── Videos/
│   └── presentation.mp4
│
├── Archives/
│   └── project.zip
│
├── Code/
│   └── script.py
│
└── Others/
    └── notes.xyz
```

## Example With Year-Month Subfolders

When **Create year-month subfolders** is enabled, files are grouped inside a folder based on the selected date rule used by the application.

```text
Downloads/
│
├── Images/
│   └── 2026-09/
│       └── photo.jpg
│
├── Documents/
│   └── 2026-09/
│       ├── assignment.pdf
│       └── data.xlsx
│
├── Audio/
│   └── 2026-09/
│       └── lecture.mp3
│
├── Videos/
│   └── 2026-09/
│       └── presentation.mp4
│
└── Archives/
    └── 2026-09/
        └── project.zip
```

## Safety Behavior

### Preview before moving

The **Preview** feature lists the files that will be organized and their proposed destination folders. It does not modify the selected folder.

### File-name conflicts

If a destination folder already contains a file with the same name, the application creates a safe alternative name instead of overwriting the existing file.

For example:

```text
photo.jpg
photo_1.jpg
photo_2.jpg
```

### Duplicate detection

The application calculates SHA-256 hashes to identify exact duplicate files. Files are considered duplicates only when their hash values match.

### Undo

The **Undo Last Operation** feature restores files moved during the most recent recorded organization operation. It does not provide unlimited history, so use the feature promptly if an organization result needs to be reversed.

### Activity logs

The app records file-organization activity in logs so that operations, file movements, and relevant errors can be reviewed later.

## Technologies Used

- Python
- Tkinter
- `pathlib`
- `shutil`
- `hashlib`
- `logging`
- `threading`
- `json`

## Future Improvements

- Drag-and-drop folder selection
- Customizable file-category settings
- Recursive organization of subfolders
- Exportable activity reports
- Duplicate-file removal after explicit user confirmation
- Automated tests
- Additional file-preview filters
- Configurable log locations and retention settings

## Contributing

Contributions, feature suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Commit the changes with a clear message.
5. Open a pull request.

## License

This project is available under the [MIT License](LICENSE).
