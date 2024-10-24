import re
import sys


def main():
    print(convert(input("Hours: ")))


def convert(s):
    # Find all occurrences of the time pattern in the given string
    matches = re.findall("(\d{1,2}):?(\d{2})? (AM|PM)", s)

    if matches:
        converted_times = []

        # Iterate over each matched time
        for match in matches:
            # Extract hours and minutes from the matched groups
            hours = int(match[0])
            minutes = int(match[1]) if match[1] else 0 # Default minutes to 0 if not provided
            am_pm = match[2]

            # Validate extracted hours and minutes
            if not (0 <= hours <= 12) or not (0 <= minutes < 60):
                raise ValueError("Invalid time format")

            if am_pm == "AM":
                if hours == 12:
                    hours = 0

            else:
                if hours < 12:
                    hours += 12

            converted_times.append(f"{hours:02d}:{minutes:02d}")

        return " to ".join(converted_times)
    else:
        raise ValueError("Invalid time format")


if __name__ == "__main__":
    main()
