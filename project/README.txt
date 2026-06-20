#####################################----IMPORTANT----#####################################

This project is a Python GUI application for importing, inspecting, filtering, and visualising
FAA Service Difficulty Report data.

How to open the application:

1. Open the project folder in a terminal.

2. Activate the virtual environment:

   Windows PowerShell:
   .\sdr_venv\Scripts\Activate.ps1

   Git Bash:
   source sdr_venv/Scripts/activate

3. Install the required libraries if needed:

   pip install -r requirements.txt

4. Go to the main folder:

   cd main

5. Start the GUI application:

   python gui.py

Important notes:

- The application should be started from the main folder when using relative image paths.
- CSV files must follow the expected FAA SDR filename format, for example: SDR-1995.csv.
- Imported data is stored in the local SQLite database inside the data folder.
- If no database exists yet, first go to the Import tab and import an SDR CSV file.
- The Data Inspection and Dashboard tabs need imported database records before they can show data.

##########################################################################################

########################################----DATA----######################################

Source: Federal Aviation Administration (FAA)
Link to source: https://www.faa.gov/av-info/download_SDR

- SDR_csvs:
    Summary:
    The Safety Defect Report / Service Difficulty Report CSV files are gathered from the FAA and are the base of this project.
    The available CSV files from the FAA are used within this project, from the year 1995 up until 2026.

- csv_to_db.py:
    Summary:
    Python script used to convert CSV data into a sqlite3 database for a more cohesive and centralized data source.
    This script can be seen as a portal between the raw CSV data and the structured database used by the application.

- SDR_database.db:
    Summary:
    SQLite database used to collect data from csv_to_db.py with CSV files gathered from the FAA.
    This database is used to inspect, filter, query, and visualise SDR data within the GUI.

##########################################################################################