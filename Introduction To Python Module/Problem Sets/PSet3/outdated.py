months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

def validate_date(date):
    m, d , y = date.split("/")
     # Validate month, day, and year
    if (
            (m in months or m.isdigit()) and
            (int(d) > 0 and int(d) < 32) and
            (int(y) and len(y) == 4)
    ):
        return True
    return False

def convert_to_iso_format(date):
    m, d, y = date.split("/")
    # Convert month to its numerical representation
    m = str(months.index(m.capitalize()) + 1).zfill(2)
     # Zero-pad the day
    d = d.zfill(2)
    # Return date in ISO format
    return f"{y}-{m}-{d}"

def main():
    while True:
        date = input("Date: ").strip()
        if validate_date(date):
            iso_date = convert_to_iso_format(date)
            print(iso_date)
            break
        else:
            print("Invalid date. Please enter a valid date.")

if __name__ == "__main__":
    main()
