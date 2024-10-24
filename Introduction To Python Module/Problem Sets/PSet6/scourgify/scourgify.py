import csv
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python scourgify.py input.csv output.csv")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Process the CSV files
    process_csv(input_file, output_file)


def process_csv(input_file, output_file):
    try:
        # Read input CSV file and store rows in a list
        with open(input_file, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            rows = [row for row in reader]
    except FileNotFoundError:
        # If the input file is not found, print an error message and exit
        print(f"Could not open file {input_file}")
        sys.exit(1)

    try:
        # Write processed data to output CSV file
        with open(output_file, "w", newline="") as csvfile:
            fieldnames = ["first", "last", "house"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in rows:
                if "name" in row and "house" in row:
                    name = row["name"].split(", ")
                    if len(row) >= 2:
                        # Write modified row to output file
                        writer.writerow(
                            {
                                "first": name[1].strip(),
                                "last": name[0],
                                "house": row["house"],
                            }
                        )
                    else:
                        # If the name field doesn't contain at least two elements, skip the row
                        print(f"Skipping invalid row: {row}")
                else:
                    # If the row doesn't contain both "name" and "house" fields, skip the row
                    print(f"Skipping invalid row: {row}")
    except Exception as e:
        # If an exception occurs while writing to the output file, print an error message and exit
        print(f"Something went wrong while writing to the output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
