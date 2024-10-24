def main():
    time = input("Enter time (in format #:## or ##:##): ")  # Get time input
    total_hours = convert(time)  # Convert to decimal hours

    # Check for meal times
    if 7.0 <= total_hours <= 8.0:
        print("It's breakfast time!")
    elif 12.0 <= total_hours <= 13.0:
        print("It's lunch time!")
    elif 18.0 <= total_hours <= 19.0:
        print("It's dinner time!")


def convert(time):
    hours, minutes = time.split(":")  # Split input into hours and minutes
    total = int(hours) + (int(minutes) / 60.0)  # Convert to decimal hours
    return total


if __name__ == "__main__":
    main()