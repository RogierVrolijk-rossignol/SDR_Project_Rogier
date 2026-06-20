"""
This python file...
1. connects to database for specific queries to gather data for graph creation.
2. creates graphs for: reports / year, reports / manufacturer, and reports / ata_chapter
"""


import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


# already creating database_name and table_name
# puts database at data directory within the project.
database_name = "../data/SDR_database.db"       
table_name = "sdr_reports"


def main():
    pass


# gets the amount of report / year using a query
def get_reports_per_year():
    # connects to database 
    conn = sqlite3.connect(database_name)

    # creates a query where amount of reports / year is extracted.
    query = f"""
    SELECT report_year, 
    COUNT(*) AS report_count 
    FROM {table_name}
    GROUP BY report_year
    ORDER BY report_year
    """

    # data is read by pandas and saved within a dataframe
    df = pd.read_sql_query(query, conn)

    # connection to database is closed
    conn.close()

    # returns the modified dataframe
    return df


# shows the results of query within a graph
def graph_reports_per_year():
    # uses dataframe from previous function
    df = get_reports_per_year()

    # configure graph size, with x and y sizes.
    plt.figure(figsize=(10, 5))
    # which columns are used to draw the graph's data
    plt.plot(df["report_year"], df ["report_count"], marker="o")

    # configures title and labels
    plt.title("Number of SDR Reports per Year")
    plt.xlabel("Year")
    plt.ylabel("Number of reports")

    # grid, and tight layout are configured before showing.
    plt.grid(True)
    # automates space between subplots.
    plt.tight_layout()
    plt.show()


# gets the amount of report / aircraft using a query with a limit of 10 aircraft.
def get_top_aircraft_makes(limit=10):
    # connects to database 
    conn = sqlite3.connect(database_name)

    # creates a query where amount of reports / aircraft manufacturer is extracted.
    query = f"""
    SELECT aircraft_make, 
    COUNT(*) AS report_count 
    FROM {table_name}
    WHERE aircraft_make IS NOT NULL
    GROUP BY aircraft_make
    ORDER BY report_count 
    DESC
    LIMIT {limit}
    """

    # data is read by pandas and saved within a dataframe
    df = pd.read_sql_query(query, conn)

    # connection to database is closed
    conn.close()

    # returns the modified dataframe
    return df


def graph_aircraft_makes():
    # uses dataframe from previous function
    df = get_top_aircraft_makes()

    # configure graph size, with x and y sizes.
    plt.figure(figsize=(10, 5))
    # which columns are used to draw the graph's data
    plt.bar(df["aircraft_make"], df["report_count"])

    # configures title and labels
    plt.title("Top 10 Aircraft Makes by SDR Reports")
    plt.xlabel("Aircraft make")
    plt.ylabel("Number of reports")

    # rotates x-axis values (aircraft makes) 45 degrees.
    plt.xticks(rotation=45)
    # automates space between subplots.
    plt.tight_layout()
    plt.show()


def get_top_ata_chapters(limit=10):
    # connects to database 
    conn = sqlite3.connect(database_name)

    # creates a query where amount of reports / ata chapter is extracted.
    query = f"""
    SELECT ata_chapter, 
    COUNT(*) AS report_count 
    FROM {table_name}
    WHERE ata_chapter IS NOT NULL
    GROUP BY ata_chapter
    ORDER BY report_count 
    DESC
    LIMIT {limit}
    """

    # data is read by pandas and saved within a dataframe
    df = pd.read_sql_query(query, conn)

    # connection to database is closed
    conn.close()

    # returns the modified dataframe
    return df


def graph_ata_chapters():
    # uses dataframe from previous function
    df = get_top_ata_chapters()

    # configures figure size
    plt.figure(figsize=(10, 5))
    # uses columns from dataframe to generate graphs
    plt.bar(df["ata_chapter"], df["report_count"])

    # configures title and labels.
    plt.title("Top 10 ATA Chapters by SDR Reports")
    plt.xlabel("ATA chapter")
    plt.ylabel("Number of reports")

    # ensures a tight layout, automates spaces between subplots before showing graph.
    plt.tight_layout()
    plt.show()


# only executes main when script is called.
if __name__ == "__main__":
    main()