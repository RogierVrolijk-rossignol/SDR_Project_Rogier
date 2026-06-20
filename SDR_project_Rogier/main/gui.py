"""
This python file...
1. is the heart of the project.
2. displays the GUI with internal functions, such as:
    
    1. toolbar
    2. home tab
    3. import tab
    4. select csv function connects to import tab
    5. import selected function connects to import
    6. inspection tab
    7. load data function connected to inspection tab
    8. clear data function connected to inspection tab
    9. dashboard tab
    10. show reports per year connects graph to dashboard tab
    11. show aircraft make connects graph to dashboard tab
    12. show ata chapters connects graph to dashboard tab
    13. ata chapters tab
    14. about tab
"""

import sys
from pathlib import Path
import sqlite3
import pandas as pd

project_folder = Path(__file__).resolve().parents[1]
sys.path.append(str(project_folder))

import data.csv_to_db as csv_to_db
import data.graph_creation as graph_creation
import data.ata_chapters as ata_chapters
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QLabel,
    QPushButton, 
    QFileDialog,
    QToolBar,
    QGroupBox,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QLineEdit
)


def main():
    # opens the GUI
    app = QApplication(sys.argv)

    # adds general styling to the GUI
    app.setStyleSheet("""
        QWidget {
            font-size: 14px;
        }

        QToolBar {
            spacing: 8px;
        }

        QLabel {
            font-size: 14px;
        }

        QPushButton {
            font-size: 14px;
            padding: 6px;
        }

        QGroupBox {
            font-weight: bold;
            margin-top: 10px;
        }
    """)

    # calls the mainwindow
    window = MainWindow()

    # shows the window
    window.show()

    # when closed program stops.
    sys.exit(app.exec())


# creating class for whole gui
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # configures basic needs, such as title, image, and dimensions
        self.setWindowTitle("Aircraft SDR Dashboard")
        self.setWindowIcon(QIcon("../images/FAA_logo.ico"))
        self.setGeometry(950, 350, 1200, 800)

        # creates a widget for mainwindow
        self.tabs = QTabWidget()

        # defines this as a central widget
        self.setCentralWidget(self.tabs)

        # creates multiple tab widgets
        self.home_tab = QWidget()
        self.import_tab = QWidget()
        self.inspection_tab = QWidget()
        self.dashboard_tab = QWidget()
        self.ata_tab = QWidget()
        self.about_tab = QWidget()

        # adds the widgets as tabs
        self.tabs.addTab(self.home_tab, "Home")
        self.tabs.addTab(self.import_tab, "Import")
        self.tabs.addTab(self.inspection_tab, "Data Inspection")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.ata_tab, "ATA Chapters")
        self.tabs.addTab(self.about_tab, "About")

        # hides the normal tab bar because navigation is done with the toolbar
        self.tabs.tabBar().hide()

        # shows a toolbar within GUI
        self.build_toolbar()

        # executes functions within tabs.
        self.build_home_tab()
        self.build_import_tab()
        self.build_inspection_tab()
        self.build_dashboard_tab()
        self.build_ata_chapters()
        self.build_about_tab()
        
        # adds styling to the statusbar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: black;
                color: white;
                font-weight: bold;
                padding: 4px;
            }
        """)

        # shows an standard message on statusbar
        # waiting for actions from user
        self.statusBar().showMessage("Ready")
        

    # creates toolbar 
    def build_toolbar(self):
        # creates a toolbar at the top of the gui application
        toolbar = QToolBar("Main Toolbar")

        # increases toolbar size and also the icon sizes.
        toolbar.setIconSize(QSize(40, 40))

        # prevents the toolbar from being moved by the user
        toolbar.setMovable(False)

        # adds the toolbar to the main window
        self.addToolBar(toolbar)

        # creates toolbar actions
        home_action = QAction(QIcon("../images/home.ico"), "Home", self)
        import_action = QAction(QIcon("../images/import_data.ico"), "Import", self)
        inspection_action = QAction(QIcon("../images/data_inspection.ico"), "Inspection", self)
        dashboard_action = QAction(QIcon("../images/dashboard.ico"), "Dashboard", self)
        ata_action = QAction(QIcon("../images/ata_chapters.ico"), "ATA Chapters", self)
        about_action = QAction(QIcon("../images/about.ico"), "About", self)

        # shows text to the user when hovered over the toolbar.
        home_action.setStatusTip("Go to Home page")
        import_action.setStatusTip("Select and import SDR CSV data")
        inspection_action.setStatusTip("Inspect rows and columns from the database")
        dashboard_action.setStatusTip("View general SDR dashboard graphs")
        ata_action.setStatusTip("View ATA chapter table")
        about_action.setStatusTip("View project information")

        # connects toolbar actions with matching tabs
        # using lambda function so whenever user switches tabs and clicks buttons an event will be executed
        # otherwise nothing will happen. 
        home_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.home_tab))
        import_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.import_tab))
        inspection_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.inspection_tab))
        dashboard_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.dashboard_tab))
        ata_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.ata_tab))
        about_action.triggered.connect(lambda: self.tabs.setCurrentWidget(self.about_tab))

        # adds actions to the toolbar
        toolbar.addAction(home_action)
        toolbar.addAction(import_action)
        toolbar.addAction(inspection_action)
        toolbar.addAction(dashboard_action)
        toolbar.addAction(ata_action)
        toolbar.addAction(about_action)


    # creating home tab functionality
    def build_home_tab(self):
        # a box layout for the home tab
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # title within the home tab
        title_label = QLabel("Aircraft SDR Dashboard")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold")

        # short subtitle under the title
        subtitle_label = QLabel("FAA Service Difficulty Report analysis tool")
        subtitle_label.setStyleSheet("font-size: 16px; color: #555555;")

        # first info box
        project_box = QGroupBox("Project Overview")
        project_layout = QVBoxLayout()

        # description text 
        project_text = QLabel(
            "\n\nWelcome to the Aircraft SDR Dashboard. \n" \
            "This application imports FAA Service Difficulty Report data " \
            "The dashboard can be used to inspect the SDR data and show graphs" \
            "about reports per year, aircraft manufacturers, and ATA chapters.\n\n" \
            "For more information please refer to the 'About' tab."
        )
        # if strings reach end of box, new line is made automatically.
        project_text.setWordWrap(True)

        # adds widget to layout
        project_layout.addWidget(project_text)
        project_box.setLayout(project_layout)

        # second information box
        usage_box = QGroupBox("Application Functions")
        usage_layout = QVBoxLayout()

        usage_text = QLabel(
            "\n\n- Import SDR CSV files into the database\n" \
            "- Inspect imported database records\n" \
            "- View dashboard graphs about SDR reports\n" \
            "- Analyse ATA chapters\n" \
            "- Read project information in the 'About' tab"
        )
        usage_text.setWordWrap(True)

        usage_layout.addWidget(usage_text)
        usage_box.setLayout(usage_layout)

        # adds widgets to the home tab layout
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addWidget(project_box)
        layout.addWidget(usage_box)

        # applies the layout to the home tab
        self.home_tab.setLayout(layout)


    # creating import tab functionality
    def build_import_tab(self):
        # a box layout for the import tab
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(12, 12, 12, 12)

        # title within the home tab
        title_label = QLabel("Import SDR CSV Data")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # description text
        description_label = QLabel(
            "Use this tab to select an FAA SDR CSV file and import it " \
            "into the SQLite database."
        )

        # creates a group box around the csv import section
        import_groupbox = QGroupBox("CSV Import")
        # using custom modifications for box layout
        # otherwise string will interfere with box. 
        import_groupbox.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #777777;
                border-radius: 4px;
                margin-top: 12px;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 4px;
                background-color: white;
            }
        """)
        import_layout = QVBoxLayout()
        import_layout.setSpacing(10)

        # label that shows selected csv file path
        self.selected_file_label = QLabel("Selected CSV file path will appear here.")
        self.selected_file_label.setStyleSheet("border: 1px solid #cccccc; padding: 6px; background-color: white;")

        # creates a horizontal layout for the two buttons.
        button_layout = QHBoxLayout()

        # adds buttons into widget
        self.select_file_button = QPushButton("Select CSV File")
        self.import_button = QPushButton("Import to Database")

        self.select_file_button.clicked.connect(self.select_csv_file)
        self.import_button.clicked.connect(self.import_selected_csv)

        button_layout.addWidget(self.select_file_button)
        button_layout.addWidget(self.import_button)

        # label that shows import messages.
        self.import_message_label = QLabel("Import messages will appear here.")
        self.import_message_label.setStyleSheet("border: 1px solid #cccccc; padding: 6px; background-color: white;")
        self.import_message_label.setMinimumHeight(240)

        # adds widgets into the groupbox layout
        import_layout.addWidget(self.selected_file_label)
        import_layout.addLayout(button_layout)
        import_layout.addWidget(self.import_message_label)

        # applies the layout to the groupbox
        import_groupbox.setLayout(import_layout)

        # adds everything to the main import tab layout
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(import_groupbox)
        layout.addStretch()
        
        self.import_tab.setLayout(layout)


    # is able to interact when user selects files within own system
    def select_csv_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "SELECT SDR CSV file","","CSV files (*.csv)")

        # creates strings to display within gui when file is selected.
        if file_path:
            self.selected_file_path = file_path
            self.selected_file_label.setText(f"Selected file: {file_path}")
            self.statusBar().showMessage("CSV file selected")
    

    # when import button is clicked this function is executed
    # it relies on csv_to_db.py
    def import_selected_csv(self):
        # checks whether the user already selected a .csv file.
        if not hasattr(self, "selected_file_path"):
            self.selected_file_label.setText("Please select a CSV file first.")
            return
        
        # gets the constants from selected file from user
        valid_file, year = csv_to_db.check_sdr_filename_and_year(self.selected_file_path)

        # if file is not valid...
        if not valid_file:
            self.selected_file_label.setText("Invalid file. Expected format: 'SDR-1995.csv'")
            return
        
        # if file doesn't exist...
        if not csv_to_db.check_file_exist(self.selected_file_path):
            self.selected_file_label.setText("Selected file does not exist")
            return
        
        # file is being read by pandas and is now called df
        df = csv_to_db.read_csv_file(self.selected_file_path)

        # if the dataframe doesn't have the required columns...
        if not csv_to_db.validate_csv_columns(df):
            self.selected_file_label.setText("CSV does not contain expected columns.")
            return
        
        # converts selected file to a source file.
        source_file = Path(self.selected_file_path).name

        # if csv (df) already in database...
        if csv_to_db.check_double_import(source_file):
            self.selected_file_label.setText("This CSV file was already imported")
            return
        
        # prepares dataframe before converting it into database.
        # this replaces columns within its right order.
        prepared_df = csv_to_db.prepare_dataframe(df, year, source_file)

        # counts the rows from database
        row_count = csv_to_db.convert_df_to_db(prepared_df)

        # shows strings with information about dataframe and database.
        self.selected_file_label.setText(
            f"CSV imported successfully.\n"
            f"Rows imported: {len(prepared_df)}\n"
            f"Total rows in database: {row_count}"
        )
        
        # shows a message within the statusbar
        self.statusBar().showMessage("Import completed")


    # inspection tab for displaying data from database and queries.
    def build_inspection_tab(self):
        # main layout for the inspection tab
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # configures title and style
        title_label = QLabel("Data Inspection")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold")

        # description label string
        description_label = QLabel("Use this tab to inspect the imported SDR data from the SQLite database.")

        # creates a groupbox for the content
        filter_groupbox = QGroupBox("Database Records")
        filter_layout = QHBoxLayout()

        # creates filter lines for year, ac make, ata, and problem
        self.year_filter_input = QLineEdit()
        self.year_filter_input.setPlaceholderText("Year e.g., '1995'")

        self.make_filter_input = QLineEdit()
        self.make_filter_input.setPlaceholderText("Aircraft make e.g., 'BOEING'")

        self.ata_filter_input = QLineEdit()
        self.ata_filter_input.setPlaceholderText("ATA chapter e.g., '27'")

        self.problem_filter_input = QLineEdit()
        self.problem_filter_input.setPlaceholderText("Problem e.g., 'CRACK'")

       # Creates buttons for loading and clearing data.
        self.load_table_button = QPushButton("Load Data")
        self.clear_table_button = QPushButton("Clear Table")

        # Connects buttons to their functions.
        self.load_table_button.clicked.connect(self.load_database_table)
        self.clear_table_button.clicked.connect(self.clear_database_table)

        # creates a table widget to show database content
        self.database_table = QTableWidget()

        # adds filters and buttons to filter layout
        filter_layout.addWidget(self.year_filter_input)
        filter_layout.addWidget(self.make_filter_input)
        filter_layout.addWidget(self.ata_filter_input)
        filter_layout.addWidget(self.problem_filter_input)
        filter_layout.addWidget(self.load_table_button)
        filter_layout.addWidget(self.clear_table_button)

        # applies layout to the groupbox
        filter_groupbox.setLayout(filter_layout)

        # displays this label when nothing is done yet.
        self.table_status_label = QLabel("No database records loaded yet.")

        self.database_table = QTableWidget()

        # adds widgets to main layout
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(filter_groupbox)
        layout.addWidget(self.table_status_label)
        layout.addWidget(self.database_table)

        # applies the layout to the inspection tab.
        self.inspection_tab.setLayout(layout)


    # uses data load function in table to display to user, when user clicks data is loaded.
    def load_database_table(self):
        # if no database has been found display string on both the box and the statusbar
        if not Path(csv_to_db.database_name).exists():
            self.table_status_label.setText("No database found. Please import a CSV File first.")
            self.statusBar().showMessage("No database found")
            return
        
        year_filter = self.year_filter_input.text().strip()
        make_filter = self.make_filter_input.text().strip()
        ata_filter = self.ata_filter_input.text().strip()
        problem_filter = self.problem_filter_input.text().strip()

        # starts the base query. WHERE 1=1 makes it easy to add filters
        query = f"SELECT * FROM {csv_to_db.table_name} WHERE 1=1"
        params = []

        # adds a year filter if entered
        if year_filter:
            query += " AND report_year LIKE ?"
            params.append(f"%{year_filter}")

        # adds a make filter if entered
        if make_filter:
            query += " AND aircraft_make LIKE ?"
            params.append(f"%{make_filter}")

        # adds a year filter if entered
        if ata_filter:
            query += " AND ata_chapter LIKE ?"
            params.append(f"%{ata_filter}")

        # adds a problem filter if entered
        if problem_filter:
            query += " AND problem_description LIKE ?"
            params.append(f"%{problem_filter}")

        query += "LIMIT 100000"

        # tries to make connection to database and execute query
        try:
            conn = sqlite3.connect(csv_to_db.database_name)
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()

        # if not able to execute because of loading display string on box and the statusbar
        except Exception as error:
            self.table_status_label.setText(f"Could not load database records.\n{error}")
            self.statusBar().showMessage("Database load failed")
            return

        # configures the table size based on the dataframe
        self.database_table.setRowCount(len(df))
        self.database_table.setColumnCount(len(df.columns))
        self.database_table.setHorizontalHeaderLabels(df.columns)

        # adds each dataframe value to the pyqt table
        for row_index in range(len(df)):
            for column_index in range(len(df.columns)):
                value = df.iloc[row_index, column_index]
                item = QTableWidgetItem(str(value))
                self.database_table.setItem(row_index, column_index, item)

        #resizes columns so the table content is easier to read.
        self.database_table.resizeColumnsToContents()

        # updates the status label and statusbar.
        if year_filter or make_filter or ata_filter or problem_filter:
            self.table_status_label.setText(f"Loaded {len(df)} filtered database records.")
            self.statusBar().showMessage("Filtered database records loaded")
        else:
            self.table_status_label.setText(f"Loaded {len(df)} database records.")
            self.statusBar().showMessage("Database records loaded")

    
    # function for clear button when user clicks data is cleared from table
    def clear_database_table(self):
        # clears all rows and columns from table
        self.database_table.clear()
        self.database_table.setRowCount(0)
        self.database_table.setColumnCount(0)

        # clears all filter input fields
        self.year_filter_input.clear()
        self.make_filter_input.clear()
        self.ata_filter_input.clear()
        self.problem_filter_input.clear()

        # updates the status label and bar
        self.table_status_label.setText("Table cleared.")
        self.statusBar().showMessage("Table cleared")


    # dashboard tab where graphs are displayed 
    def build_dashboard_tab(self):
        # main layout for the inspection tab
        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        # configures title and style
        title_label = QLabel("Dashboard")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold")

        # description label string
        description_label = QLabel("Use this tab to display general SDR dashboard graphs.")

        # creates a groupbox for the content
        dashboard_groupbox = QGroupBox("Dashboard graphs")
        dashboard_layout = QHBoxLayout()

        # creates buttons for graph selection
        button_layout = QVBoxLayout()

        self.reports_year_button = QPushButton("Reports per Year")
        self.aircraft_make_button = QPushButton("Top Aircraft Makes")
        self.ata_chapter_button = QPushButton("Top ATA Chapters")

        self.reports_year_button.clicked.connect(self.show_reports_per_year_graph)
        self.aircraft_make_button.clicked.connect(self.show_aircraft_makes_graph)
        self.ata_chapter_button.clicked.connect(self.show_ata_chapters_graph)

        button_layout.addWidget(self.reports_year_button)
        button_layout.addWidget(self.aircraft_make_button)
        button_layout.addWidget(self.ata_chapter_button)

        # creates matplotfigure and canvas
        self.dashboard_figure = Figure(figsize=(8, 5))
        self.dashboard_canvas = FigureCanvas(self.dashboard_figure)

        # adds widgets to dashboard layout
        dashboard_layout.addLayout(button_layout)
        dashboard_layout.addWidget(self.dashboard_canvas)

        # applies layout to groupbox
        dashboard_groupbox.setLayout(dashboard_layout)

        # adds widgets to main tab layout
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(dashboard_groupbox)

        #applies layout to dashboard tab
        self.dashboard_tab.setLayout(layout)

    
    # shows the amount reports within a graph for each year
    def show_reports_per_year_graph(self):
        # clears current dashboard figure
        self.dashboard_figure.clear()

        # gets data from graph_creation.py
        df = graph_creation.get_reports_per_year()

        # adds a subplot to the figure
        ax = self.dashboard_figure.add_subplot(111)

        # creates a line graph
        ax.plot(df["report_year"], df["report_count"], marker="o")

        # shows only full years on the x-axis.
        ax.set_xticks(df["report_year"])
        ax.set_xticklabels(df["report_year"].astype(int))

        # sets graph titles ands labels
        ax.set_title("Number of SDR Reports per Year")
        ax.set_xlabel("Year")
        ax.set_ylabel("Number of Reports")
        ax.grid(True)

        # rotates labels so a/c names are readable
        ax.tick_params(axis="x", rotation=45)

        # makes layout fit better inside the canvas
        self.dashboard_figure.tight_layout()

        # redraws the canvas inside the gui
        self.dashboard_canvas.draw()

        # updates the statusbar
        self.statusBar().showMessage("Reports per year graph loaded")


    # shows the top aircraft manufacturers that've report counts, this is displayed within a graph
    def show_aircraft_makes_graph(self):
        # clears current dashboard figure
        self.dashboard_figure.clear()

        # gets data from graph_creation.py
        df = graph_creation.get_top_aircraft_makes()

        # adds a subplot to the figure
        ax = self.dashboard_figure.add_subplot(111)

        # creates a bar graph
        ax.bar(df["aircraft_make"], df["report_count"])

        # sets graph titles ands labels
        ax.set_title("Top 10 Aircraft Makes by SDR Reports")
        ax.set_xlabel("Aircraft Make")
        ax.set_ylabel("Number of Reports")
        ax.grid(True)

        # rotates labels so a/c names are readable
        ax.tick_params(axis="x", rotation=45)

        # makes layout fit better inside the canvas
        self.dashboard_figure.tight_layout()

        # redraws the canvas inside the gui
        self.dashboard_canvas.draw()

        # updates the statusbar
        self.statusBar().showMessage("Aircraft makes graph loaded")


    # shows the top ata chapters within a graph 
    def show_ata_chapters_graph(self):
        # clears current dashboard figure
        self.dashboard_figure.clear()

        # gets data from graph_creation.py
        df = graph_creation.get_top_ata_chapters()

        # adds a subplot to the figure
        ax = self.dashboard_figure.add_subplot(111)

        # creates a line graph
        ax.bar(df["ata_chapter"], df["report_count"])

        # sets graph titles ands labels
        ax.set_title("Top 10 ATA Chapters by SDR Reports")
        ax.set_xlabel("ATA Chapter")
        ax.set_ylabel("Number of Reports")
        ax.grid(True)

        # makes layout fit better inside the canvas
        self.dashboard_figure.tight_layout()

        # redraws the canvas inside the gui
        self.dashboard_canvas.draw()

        # updates the statusbar
        self.statusBar().showMessage("Top ATA Chapters graph loaded")

    # shows the ata chapters in table
    def build_ata_chapters(self):
        # main layout for the ATA tab.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # title for tab
        title_label = QLabel("ATA Chapters")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold")

        # description for tab
        description_label = QLabel("ATA chapters are standard aviation maintenance categories used to group aircraft systems")

        # creates a groupbox for table
        ata_groupbox = QGroupBox("ATA Chapter Overview")
        ata_layout = QVBoxLayout()

        #creates the table for ata_chapters.py
        self.ata_table = QTableWidget()

        # gets data from ata_chapters.py
        ata_data = ata_chapters.get_ata_chapters()

        # configures table size
        self.ata_table.setRowCount(len(ata_data))
        self.ata_table.setColumnCount(2)
        self.ata_table.setHorizontalHeaderLabels(["ATA Chapter", "System Description"])

        # fills the table with ata chapter data
        for row_index, (chapter, description) in enumerate(ata_data.items()):
            self.ata_table.setItem(row_index, 0, QTableWidgetItem(chapter))
            self.ata_table.setItem(row_index, 1, QTableWidgetItem(description))

        # makes columns easier to read
        self.ata_table.resizeColumnsToContents()

        #adds widgets to ata tab
        ata_layout.addWidget(self.ata_table)
        ata_groupbox.setLayout(ata_layout)

        # adds widgets to tab
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(ata_groupbox)

        # applies the layout to tab
        self.ata_tab.setLayout(layout)


    # about tab, where information is stored about project
    def build_about_tab(self):
        # main layout for the About tab.
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # title for the About tab.
        title_label = QLabel("About This Application")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold;")

        # project information box.
        about_box = QGroupBox("Project Summary")
        about_layout = QVBoxLayout()

        # text to be displayed about project information
        about_text = QLabel(
            "\n\nAircraft SDR Dashboard is a Python application for importing, inspecting, " \
            "filtering, and visualising FAA Service Dificulty Report data \n" \
            "The tool supports aviation engineering making technical report data easier" \
            "to analyse. It helps identify trends by year, aircraft manufacturer, and ATA chapter.\n\n" \
            "Used libraries:\n- PyQt6 \n- pandas \n- SQLite \n- pathlib \n- matplotlib"
        )
        about_text.setWordWrap(True)

        about_layout.addWidget(about_text)
        about_box.setLayout(about_layout)

        # adds widgets to about tab
        layout.addWidget(title_label)
        layout.addWidget(about_box)

        # applies the layout to the about tab.
        self.about_tab.setLayout(layout)
        

if __name__ == "__main__":
    main()