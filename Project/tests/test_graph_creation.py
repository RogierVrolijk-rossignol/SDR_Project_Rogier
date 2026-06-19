"""
This python file...
- tests data supported python script (graph_creation.py).

Some processes are mimicked from the original files, such as databases and dataframes. 
This is to test whether certain function work the way it's supposed to.

COMMAND: "python -m pytest tests/test_graph_creation.py -v"
"""


import sqlite3
import pandas as pd
import data.graph_creation as graph # to check .py for graph creation


# test dataframe is used.
def make_graph_df():
    df = pd.DataFrame({
        "report_year": [1995, 1995, 1996],
        "source_file": ["SDR-1995.csv", "SDR-1995.csv", "SDR-1996.csv"],
        "difficulty_date": ["1995-01-01", "1995-01-02", "1996-01-01"],
        "aircraft_make": ["BOEING", "BOEING", "AIRBUS"],
        "aircraft_model": ["737", "737", "A320"],
        "ata_code": [2730, 2730, 3210],
        "ata_chapter": ["27", "27", "32"],
        "part_name": ["FLAP", "FLAP", "GEAR"],
        "part_number": ["123", "123", "456"],
        "problem_description": ["Problem 1", "Problem 2", "Problem 3"]
    })

    return df


# tests query for year data
def test_graph_year_query(tmp_path):
    # uses test dataframe
    df = make_graph_df()

    # creates a temporary database
    test_database = tmp_path / "test_sdr.db"
    # connects to temporary database
    conn = sqlite3.connect(test_database)

    # dataframe to temporary database
    df.to_sql("sdr_reports", conn, if_exists="append", index=False)

    graph.database_name = test_database

    # gets query result
    result = graph.get_reports_per_year()

    # database connection is closed
    conn.close()

    # checks whether these requirements are met.
    assert result.loc[0, "report_year"] == 1995
    assert result.loc[0, "report_count"] == 2


# tests query for manufacturer data
def test_graph_make_query(tmp_path):
    # uses test dataframe
    df = make_graph_df()

    # creates a temporary database
    test_database = tmp_path / "test_sdr.db"
    # connects to temporary database
    conn = sqlite3.connect(test_database)

    # dataframe to temporary database
    df.to_sql("sdr_reports", conn, if_exists="append", index=False)

    graph.database_name = test_database

    # gets query result
    result = graph.get_top_aircraft_makes()

    # database connection is closed
    conn.close()

    # checks whether these requirements are met.
    assert result.loc[0, "aircraft_make"] == "BOEING"
    assert result.loc[0, "report_count"] == 2


# tests query for ata data
def test_graph_ata_query(tmp_path):
    # uses test dataframe
    df = make_graph_df()

    # creates a temporary database
    test_database = tmp_path / "test_sdr.db"
    # connects to temporary database
    conn = sqlite3.connect(test_database)

    # dataframe to temporary database
    df.to_sql("sdr_reports", conn, if_exists="append", index=False)

    graph.database_name = test_database

    # gets query result
    result = graph.get_top_ata_chapters()

    # database connection is closed
    conn.close()

    # checks whether these requirements are met.
    assert result.loc[0, "ata_chapter"] == "27"
    assert result.loc[0, "report_count"] == 2