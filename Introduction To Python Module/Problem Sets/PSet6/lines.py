import os
import sys


def main():
    if len(sys.argv) != 2:
        print("Usage: python lines.py [file]")
        sys.exit(1)

    file_name = sys.argv[1]
    if not file_name.endswith(".py") or not os.path.isfile(file_name):
        print(f"File {file_name} does not exist or is not a Python file.")
        sys.exit(1)

    # Read the file line by line
    with open(file_name, "r") as f:
        lines = f.readlines()

    count = 0
    for line in lines:
        stripped_line = line.strip()
        # Skip comments and empty lines
        if not stripped_line.startswith("#") and stripped_line != "":
            count += 1

    print(f"Number of lines of code: {count}")


if __name__ == "__main__":
    main()
