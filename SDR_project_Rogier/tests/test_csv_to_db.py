"""
This python file...
- tests data supported python script (csv_to_db.py).

Some processes are mimicked from the original files, such as databases and dataframes. 
This is to test whether certain function work the way it's supposed to.

COMMAND: "python -m pytest tests/test_csv_to_db.py -v"
"""


import sqlite3
import pandas as pd
import data.csv_to_db as csv_to_db # to check .py for data transfer


# a test dataframe
def make_test_df():
    df = pd.DataFrame({
        "DifficultyDate": ["1995-01-01"],
        "AircraftMake": ["BOEING"],
        "AircraftModel": ["737"],
        "JASCCode": [2730],
        "PartName": ["FLAP"],
        "PartNumber": ["123"],
        "Discrepancy": ["Problem text"]
    })

    return df


# tests file name.
def test_filename_valid():
    valid_file, year = csv_to_db.check_sdr_filename_and_year("SDR-1995.csv")

    # expects a correct outcome.
    assert valid_file == True
    # correct year within string is returned
    assert year == 1995


# tests file name based on a wrong input.
def test_filename_invalid():
    valid_file, year = csv_to_db.check_sdr_filename_and_year("wrong.csv")

    # outcome should be false.
    assert valid_file == False
    # no year is added as well.
    assert year is None


# test whether columns is valid
def test_columns_valid():
    # uses test dataframe
    df = make_test_df()

    # uses validation function to check
    result = csv_to_db.validate_csv_columns(df)

    # outcome should be True, meaning dataframe is correct
    assert result == True


# tests whether column titles are converted correctly
def test_prepare_dataframe():
    # uses test dataframe
    df = make_test_df()

    # uses correct input variables.
    prepared_df = csv_to_db.prepare_dataframe(df, 1995, "SDR-1995.csv")

    # checks if datatype can be inserted within columns.
    # or that it will be cancelled due to expected data type.
    assert prepared_df.loc[0, "report_year"] == 1995
    assert prepared_df.loc[0, "source_file"] == "SDR-1995.csv"
    assert prepared_df.loc[0, "ata_chapter"] == "27"
    assert "problem_description" in prepared_df.columns


# tests if data can be inserted within database.
def test_database_insert(tmp_path):
    # uses test dataframe
    df = make_test_df()
    # tests the prepare dataframe function with the required input constants.
    prepared_df = csv_to_db.prepare_dataframe(df, 1995, "SDR-1995.csv")

    # makes a test database instead of using the initial one.
    test_database = tmp_path / "test_sdr.db"

    # connects to database
    conn = sqlite3.connect(test_database)

    # uses pandas to connect to database
    prepared_df.to_sql("sdr_reports", conn, if_exists="append", index=False)

    # uses cursor for queries
    cursor = conn.cursor()
    # query for amount of rows from database
    cursor.execute("SELECT COUNT(*) FROM sdr_reports")
    row_count = cursor.fetchone()[0]

    # closes database connection
    conn.close()

    # amount of rows needs to be equal to one.
    assert row_count == 1


# tests database content
def test_database_values(tmp_path):
    # uses test dataframe
    df = make_test_df()
    # uses the prepare dataframe function with correct input constants
    prepared_df = csv_to_db.prepare_dataframe(df, 1995, "SDR-1995.csv")

    # creates a test database instead of the initial one.
    test_database = tmp_path / "test_sdr.db"

    # connects to database
    conn = sqlite3.connect(test_database)

    # pandas to database
    prepared_df.to_sql("sdr_reports", conn, if_exists="append", index=False)

    # uses cursor for queries
    cursor = conn.cursor()
    # executes the query where data is fetched 
    cursor.execute(
        "SELECT report_year, source_file, aircraft_make, ata_chapter FROM sdr_reports"
    )

    # fetched data becomes result
    result = cursor.fetchone()

    # connection is closed from database
    conn.close()

    # checks whether result is equal to data.
    # if so; passed.
    assert result == (1995, "SDR-1995.csv", "BOEING", "27")

    