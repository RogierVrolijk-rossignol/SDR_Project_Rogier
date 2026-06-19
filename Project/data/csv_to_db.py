"""
This python file...
1. asks the user for input data (sdr .csv).
2. checks if filename and year digit is valid based on expectations. 
3. checks if file does exist by the given path.
4. reads a csv file using pandas.
5. checks csv for expected columns.
6. checks whether file inserted by user is not already in database.
7. prepares dataframe before committed to database.
8. commits dataframe to sql database.
"""


from pathlib import Path
import pandas as pd
import sqlite3


# already creating database_name and table_name
# puts database at data directory within the project.
database_name = "../data/SDR_database.db"       
table_name = "sdr_reports"


# this dict changes current column titles to newer cohesive ones.
# this is on top of script so I can reuse this more easy.
change_of_column_titles = {
    "DifficultyDate": "difficulty_date",
    "AircraftMake": "aircraft_make",
    "AircraftModel": "aircraft_model",
    "JASCCode": "ata_code",
    "PartName": "part_name",
    "PartNumber": "part_number",
    "Discrepancy": "problem_description"
}


def main():
    # asks user for a filename.
    # if file is in other folder add the required path before the file.
    file_name = input("Insert CSV filename e.g., 'SDR-1995.csv': ").strip()
    source_file = Path(file_name).name

    valid_file, year = check_sdr_filename_and_year(file_name)

    if not valid_file:
        print("Invalid filename\n")
        return
    
    if not check_file_exist(file_name):
        print("File does not exist\n")
        return
    
    df = read_csv_file(file_name)

    if not validate_csv_columns(df):
        print("CSV does not contain expected columns.\n")
        return

    if check_double_import(source_file):
        print("This CSV file was already imported.\n")
        return

    df = prepare_dataframe(df, year, Path(file_name).name)

    quantity_rows_db = convert_df_to_db(df)

    print(f"CSV imported into database {database_name}\n")
    print(f"Rows imported: {len(df)}")
    
    print(f"Current database database rows: {quantity_rows_db} ")


# checks if csv filename corresponds with expected name.
def check_sdr_filename_and_year(file_path):
    # creates a object from filepath
    file_path = Path(file_path)
    # only picks the filename + type of file
    file_name = file_path.name

    # if filename doesn't start with...
    if not file_name.startswith("SDR-"):
        return False, None
    
    # if filename doesn't end with...
    if not file_name.endswith(".csv"):
        return False, None

    # subtracts the two parts of the string.
    year_text = file_name.replace("SDR-", "").replace(".csv", "")

    # if the leftover of the string is not digit...
    if not year_text.isdigit():
        return False, None
    
    # if True, convert to integer instead of string.
    year = int(year_text)

    # if years are not within boundaries...
    if year < 1995 or year >2026:
        return False, None
    
    # if all conditions are met as required return True.
    # this function also returns year since it will be inserted in database.
    return True, year


# checks if file does exist in path.
def check_file_exist(file_path):
    # creates a object from the filepath.
    file_path = Path(file_path)

    # if file path doesn't exist on system of user...
    if not file_path.exists():
        return False
    
    # if statement was met return True.
    return True


# reads the csv file using pandas.
def read_csv_file(file_path):
    # creates a object from the filepath.
    file_path = Path(file_path)
    # reads csv using pandas without low memory.
    # meaning pandas reads cells with more care.
    df = pd.read_csv(file_path, low_memory=False)

    # if CSV is read return dataframe
    return df


def validate_csv_columns(df):
    # for the titles in current columns...
    for column_title in change_of_column_titles.keys(): # 'change_of_column_titles' is on top of script
        # if column title not in current columns...
        if column_title not in df.columns:
            return False
        
    return True


def prepare_dataframe(df, year, source_file):
    # copies the dataframe instead of modifying it directly.
    df = df.copy()
    # selects original columns
    df = df[list(change_of_column_titles.keys())] # 'change_of_column_titles' is on top of script
    # current column titles are being renamed for the newer ones.
    df = df.rename(columns = change_of_column_titles)

    # "report_year" column is now the first column in order with "year" as value.
    df.insert(0, "report_year", year)
    # adds a column title for source file. 
    df.insert(1,"source_file", source_file)

    # creates ata chapter from the first two digits from ata_code.
    ata_chapter = df["ata_code"].astype(str).str[:2]
    df.insert(6, "ata_chapter", ata_chapter)

    return df


def check_double_import(source_file):
    # connects to database
    conn = sqlite3.connect(database_name)
    # using cursor for queries
    cursor = conn.cursor()

    # query checks whether table already exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))

    # create a object from table
    table_exists = cursor.fetchone()

    if table_exists is None:
        conn.close()
        return False
    
    # checks whether source file (CSV) is already imported within database.
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE source_file = ?", (source_file,))

    # create a object from the result
    result = cursor.fetchone()[0]

    conn.close()

    if result > 0:
        return True
    
    return False


def convert_df_to_db(df):
    # connects to database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # converts CSV dataframe towards database.
    df.to_sql(table_name, conn, if_exists="append",  index=False)

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}") # 'table_name' is on top of script.

    quantity_rows_db = cursor.fetchone()[0]

    # closes connection to database.
    conn.close()

    return quantity_rows_db


# only executes main when script is called.
if __name__ == "__main__":
    main()