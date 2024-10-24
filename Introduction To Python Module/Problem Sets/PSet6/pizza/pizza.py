import csv
import sys
import os
from tabulate import tabulate


def main():
    if len(sys.argv) != 2:
        print("Usage python pizza.py <filename>")
        sys.exit()

    filename = sys.argv[1]
    if not filename.endswith(".csv"):
        print("File must be a .csv")
        sys.exit()

    # Read the CSV file
    with open(filename, "r") as file:
        reader = csv.reader(file)
        header = next(reader) # Extract header
        data = list(reader)   # Extract data

    # Use tabulate to format the CSV data as a table and print it
    table = tabulate(data, headers=header, tablefmt="grid")
    print(table)


if __name__ == "__main__":
    main()
