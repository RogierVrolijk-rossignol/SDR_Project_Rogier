"""
This python file...
- tests data supported python script (gui.py).

COMMAND: "pytest test_gui.py -v".
"""

import sys
from pathlib import Path

project_folder = Path(__file__).resolve().parents[1]

sys.path.append(str(project_folder))
sys.path.append(str(project_folder / "main"))

from gui import MainWindow


# tests if the main window can be created
def test_main_window_opens(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "Aircraft SDR Dashboard"


# tests if the expected tabs are created
def test_tabs_created(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.tabs.count() == 6


# tests if the tab bar is hidden because toolbar navigation is used
def test_tab_bar_hidden(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.tabs.tabBar().isHidden() == True


# tests if the import tab has the required buttons
def test_import_buttons_exist(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.select_file_button.text() == "Select CSV File"
    assert window.import_button.text() == "Import to Database"


# tests if the data inspection filter fields exist
def test_data_inspection_filters_exist(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.year_filter_input.placeholderText() == "Year e.g., '1995'"
    assert window.make_filter_input.placeholderText() == "Aircraft make e.g., 'BOEING'"
    assert window.ata_filter_input.placeholderText() == "ATA chapter e.g., '27'"
    assert window.problem_filter_input.placeholderText() == "Problem e.g., 'CRACK'"


# tests if the clear table button clears the table and filter fields
def test_clear_database_table(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.year_filter_input.setText("1995")
    window.make_filter_input.setText("BOEING")
    window.ata_filter_input.setText("27")
    window.problem_filter_input.setText("CRACK")

    window.clear_database_table()

    assert window.year_filter_input.text() == ""
    assert window.make_filter_input.text() == ""
    assert window.ata_filter_input.text() == ""
    assert window.problem_filter_input.text() == ""
    assert window.database_table.rowCount() == 0
    assert window.database_table.columnCount() == 0