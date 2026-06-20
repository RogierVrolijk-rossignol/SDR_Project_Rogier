"""
TITANIC GRAPH ASSIGNMENT

This Python file creates a graph from titanic.csv.

The program works in this order:
1. It reads titanic.csv.
2. It calculates passenger counts by age.
3. It creates four graph lines:
   - Female survivors
   - Female total passengers
   - Male survivors
   - Male total passengers
4. It saves the graph as a PNG file.
5. It saves the processed graph data as a CSV file.
"""


import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# Creates the output folder if it does not exist.
def create_output_folder():
    # Sets the output folder path.
    output_folder = Path("output")

    # Creates the output folder.
    output_folder.mkdir(exist_ok=True)

    # Returns the output folder path.
    return output_folder


# Reads the Titanic CSV file.
def read_titanic_csv(csv_path):
    # Reads the CSV file into a pandas DataFrame.
    data = pd.read_csv(csv_path)

    # Returns the DataFrame.
    return data


# Counts passengers per age based on a filter.
def get_age_counts(data, mask):
    # Converts the Age column to numbers.
    ages = pd.to_numeric(data["Age"], errors="coerce")

    # Selects the ages that match the mask.
    selected_ages = ages[mask].dropna()

    # Creates age bins from 0 to 100.
    bins = list(range(0, 101))

    # Creates age labels from 0 to 99.
    age_labels = list(range(0, 100))

    # Counts passengers per age group.
    counts = (
        pd.cut(selected_ages, bins=bins, right=False, labels=age_labels)
        .value_counts()
        .sort_index()
    )

    # Makes sure all ages from 0 to 99 are included.
    counts = counts.reindex(age_labels, fill_value=0)

    # Returns the counts as a list.
    return counts.tolist()


# Calculates all graph data.
def calculate_graph_data(data):
    # Converts the Sex column to lowercase text.
    sex = data["Sex"].astype(str).str.lower()

    # Converts the Survived column to numbers.
    survived = pd.to_numeric(data["Survived"], errors="coerce")

    # Creates the x-axis ages.
    ages = list(range(0, 100))

    # Calculates female survivors.
    female_survivors = get_age_counts(
        data,
        (sex == "female") & (survived == 1)
    )

    # Calculates female total passengers.
    female_total = get_age_counts(
        data,
        sex == "female"
    )

    # Calculates male survivors.
    male_survivors = get_age_counts(
        data,
        (sex == "male") & (survived == 1)
    )

    # Calculates male total passengers.
    male_total = get_age_counts(
        data,
        sex == "male"
    )

    # Returns all calculated graph data.
    return ages, female_survivors, female_total, male_survivors, male_total


# Creates and saves the Titanic graph.
def create_graph(ages, female_survivors, female_total, male_survivors, male_total, output_folder):
    # Creates the figure size.
    plt.figure(figsize=(12, 6))

    # Adds the four graph lines.
    plt.plot(ages, female_survivors, label="Female survivors")
    plt.plot(ages, female_total, label="Female total passengers")
    plt.plot(ages, male_survivors, label="Male survivors")
    plt.plot(ages, male_total, label="Male total passengers")

    # Adds title and labels.
    plt.title("Titanic passengers by age and sex")
    plt.xlabel("Age")
    plt.ylabel("Amount of passengers")

    # Sets the x-axis range.
    plt.xlim(0, 100)

    # Adds a legend and grid.
    plt.legend()
    plt.grid(True)

    # Improves layout.
    plt.tight_layout()

    # Sets the graph output path.
    graph_path = output_folder / "titanic_lines.png"

    # Saves the graph.
    plt.savefig(graph_path)

    # Closes the graph.
    plt.close()

    # Prints feedback.
    print("Graph saved:", graph_path)


# Saves the processed graph data as a CSV file.
def save_processed_data(ages, female_survivors, female_total, male_survivors, male_total, output_folder):
    # Creates a DataFrame with the calculated graph data.
    processed_data = pd.DataFrame({
        "age": ages,
        "female_survivors": female_survivors,
        "female_total": female_total,
        "male_survivors": male_survivors,
        "male_total": male_total
    })

    # Sets the CSV output path.
    data_path = output_folder / "titanic_lines_data.csv"

    # Saves the processed data as CSV.
    processed_data.to_csv(data_path, index=False)

    # Prints feedback.
    print("Processed data saved:", data_path)


# Main function of the program.
def main():
    # Sets the CSV file path.
    csv_path = "titanic.csv"

    # Creates the output folder.
    output_folder = create_output_folder()

    # Reads the Titanic CSV file.
    data = read_titanic_csv(csv_path)

    # Calculates the graph data.
    ages, female_survivors, female_total, male_survivors, male_total = calculate_graph_data(data)

    # Creates and saves the graph.
    create_graph(
        ages,
        female_survivors,
        female_total,
        male_survivors,
        male_total,
        output_folder
    )

    # Saves the processed data.
    save_processed_data(
        ages,
        female_survivors,
        female_total,
        male_survivors,
        male_total,
        output_folder
    )


# Makes sure main() only runs when this file is executed directly.
if __name__ == "__main__":
    main()