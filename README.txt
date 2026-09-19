SMART FILE ORGANIZER
====================

A Python desktop application that automatically organizes files into category folders. The project follows the Model-View-Controller (MVC) architecture and uses Python's built-in standard library.


FEATURES
--------

- Preview files before moving anything
- Organize files by extension into category folders
- Automatically create required destination folders
- Optional organization into year-month subfolders
- Safely rename conflicting files instead of overwriting them
- Detect exact duplicate files using SHA-256 hashes
- Save activity logs
- Undo the most recent organization operation
- Simple Tkinter desktop graphical interface


FILE CATEGORIES
---------------

Images:
.jpg, .jpeg, .png, .gif, .bmp, .webp, .svg, .tiff

Documents:
.pdf, .doc, .docx, .txt, .rtf, .odt, .xls, .xlsx, .ppt, .pptx, .csv

Videos:
.mp4, .mkv, .avi, .mov, .wmv, .flv, .webm

Audio:
.mp3, .wav, .flac, .aac, .ogg, .m4a

Archives:
.zip, .rar, .7z, .tar, .gz, .bz2

Code:
.py, .js, .ts, .html, .css, .json, .xml, .java, .c, .cpp, .php, .sql

Others:
Any file type not included in the categories above.


PROJECT STRUCTURE
-----------------

SmartFileOrganizer/
|
|-- main.py
|-- README.txt
|-- .gitignore
|-- LICENSE
|-- pyproject.toml
|-- uv.lock
|
|-- controllers/
|   |-- __init__.py
|   `-- organizer_controller.py
|
|-- models/
|   |-- __init__.py
|   `-- organizer_model.py
|
`-- views/
    |-- __init__.py
    `-- organizer_view.py


MVC ARCHITECTURE
----------------

main.py starts the application and connects all MVC components.

Model: models/organizer_model.py
- Scans folders
- Identifies file extensions
- Categorizes files
- Creates folders
- Moves files
- Detects duplicates
- Creates activity logs
- Handles undo operations

View: views/organizer_view.py
- Creates the Tkinter GUI
- Displays buttons, folder selector, preview table, and messages

Controller: controllers/organizer_controller.py
- Responds to button clicks
- Connects the View and Model
- Updates the interface with results and errors


REQUIREMENTS
------------

- Python 3.10 or later recommended
- Tkinter (normally included with Python)
- No external Python packages are required


HOW TO RUN
----------

Open a terminal in the project folder and run:

python main.py

On some systems, use:

python3 main.py

For Windows PowerShell using the virtual environment:

.\.venv\Scripts\python.exe .\main.py

Do not run organizer_model.py, organizer_view.py, or organizer_controller.py directly. Always run main.py.


HOW TO USE
----------

1. Run main.py.
2. Click Browse and choose a folder to organize.
3. Click Preview to see files and proposed destinations. Preview does not move files.
4. Optionally select Create year-month subfolders.
5. Click Organize Files and confirm the action.
6. Click Find Duplicates to search for files with matching SHA-256 hashes.
7. Click Undo Last Operation to restore files from the latest organization operation.

IMPORTANT: Test the app with a copied test folder before using it on important files. Undo applies only to the latest recorded operation.


EXAMPLE RESULT
--------------

Downloads/
|-- Images/
|   `-- photo.jpg
|-- Documents/
|   |-- assignment.pdf
|   `-- data.xlsx
|-- Audio/
|   `-- lecture.mp3
|-- Videos/
|   `-- presentation.mp4
`-- Archives/
    `-- project.zip


TECHNOLOGIES USED
-----------------

- Python
- Tkinter
- pathlib
- shutil
- hashlib
- logging
- threading
- JSON


FUTURE IMPROVEMENTS
-------------------

- Drag-and-drop folder selection
- Custom file-category settings
- Recursive organization of subfolders
- Exportable activity reports
- Duplicate-file removal after user confirmation
- Automated tests


LICENSE
-------

This project is available under the MIT License.
