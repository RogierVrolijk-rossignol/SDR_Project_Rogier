"""
ASSIGNMENT ONE
1. Start with asking for a file name
2. Start searching at the User Document Dir
3. The application has a global variable for a list that in the end contains all absolute paths to the found files
4. Iterate through all folders, deeper and deeper. You may want to use recursion for this.
5. IMPORTANT: ignore all filenames and dirnames starting with a . (a dot).
6. At the end, use pretty print (pprint library) to print the list with absolute paths.
"""

"""
ASSIGNMENT TWO
1. Store file on several places within the Documents dir manually.
2. Use first assignment function to progress within assignment two.
3. Delete all found files.
"""

"""
ASSIGNMENT THREE
1. Create a GUI field.
2. A button to start the search.
3. A list or table to show all found files.
4. If clicked on rows in table / list it opens the folder holding the file in explorer.
"""

import sys
import subprocess
from pathlib import Path
from pprint import pprint

from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QLineEdit,
    QListWidget,
    QVBoxLayout,
    QWidget,
    QLabel,
)


# Global variable for all found absolute paths
found_files = []


def get_start_folder():
    """
    Returns the Documents folder of the current user.
    This keeps the program safer than searching the whole computer.
    """
    return Path.home() / "Documents"


def search_folder(folder, lookfor):
    """
    Recursively search through folders for a file with the given name.
    Ignore files and folders starting with a dot.
    """

    try:
        for item in folder.iterdir():

            # Ignore files and folders starting with a dot
            if item.name.startswith("."):
                continue

            # If item is a file, check if the name matches
            if item.is_file():
                if item.name == lookfor:
                    found_files.append(str(item.absolute()))

            # If item is a folder, search deeper using recursion
            elif item.is_dir():
                search_folder(item, lookfor)

    except PermissionError:
        # Ignore folders where access is denied
        pass


def assignment_one():
    """
    Terminal version:
    ask for filename, search in Documents, print found files with pprint.
    """

    found_files.clear()

    lookfor = input("filename: ").strip()
    start_folder = get_start_folder()

    search_folder(start_folder, lookfor)

    print("\nFound files:")
    pprint(found_files)


def assignment_two():
    """
    Terminal version:
    ask for filename, search in Documents, delete found files,
    search again and print the result.
    """

    found_files.clear()

    lookfor = input("filename to delete: ").strip()
    start_folder = get_start_folder()

    search_folder(start_folder, lookfor)

    print("\nFound files before deleting:")
    pprint(found_files)

    for file_path in found_files:
        path = Path(file_path)

        try:
            path.unlink()
            print("Deleted:", path)

        except PermissionError:
            print("No permission to delete:", path)

        except FileNotFoundError:
            print("File already deleted:", path)

    found_files.clear()
    search_folder(start_folder, lookfor)

    print("\nFound files after deleting:")
    pprint(found_files)


def open_file_folder(file_path):
    """
    Opens the folder that contains the selected file.
    This works on Windows.
    """

    path = Path(file_path)

    if path.exists():
        subprocess.Popen(f'explorer /select,"{path}"')


def assignment_three():
    """
    GUI version:
    search for a filename using a field and button.
    Show results in a list.
    Double-click a result to open the file location in Explorer.
    """

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()

            self.setWindowTitle("File Searcher")
            self.setMaximumSize(QSize(800, 500))
            self.setMinimumSize(QSize(400, 300))

            self.info_label = QLabel("Search starts in your Documents folder.")

            self.input_field = QLineEdit()
            self.input_field.setPlaceholderText("Enter filename, for example test.txt")

            self.search_button = QPushButton("Search")
            self.search_button.clicked.connect(self.start_search)

            self.result_list = QListWidget()
            self.result_list.itemDoubleClicked.connect(self.open_selected_file_folder)

            layout = QVBoxLayout()
            layout.addWidget(self.info_label)
            layout.addWidget(self.input_field)
            layout.addWidget(self.search_button)
            layout.addWidget(self.result_list)

            container = QWidget()
            container.setLayout(layout)

            self.setCentralWidget(container)

        def start_search(self):
            found_files.clear()
            self.result_list.clear()

            lookfor = self.input_field.text().strip()
            start_folder = get_start_folder()

            search_folder(start_folder, lookfor)

            for file_path in found_files:
                self.result_list.addItem(file_path)

        def open_selected_file_folder(self, item):
            file_path = item.text()
            open_file_folder(file_path)

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()


def main():
    assignment_three()


if __name__ == "__main__":
    main()