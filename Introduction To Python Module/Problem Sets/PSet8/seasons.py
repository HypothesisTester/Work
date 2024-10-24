from datetime import date
import sys
from num2words import num2words


def main():
    birth_date = input("Please enter your birth date in YYYY-MM-DD format: ")
    try:
        # Convert string input to a date object
        birth_date = datetime.striptime.strptime(birth_date, "%Y-%m-d").date()
    except ValueError:
        sys.exit("Invalid date format")

    age_in_minutes = calculate_age_in_minutes(birth_date)
    age_in_words = convert_to_words(age_in_minutes)

    print(f"{age_in_words} minutes")


def calculate_age_in_minutes(birth_date):
    today = date.today()
    age_in_days = (today - birth_date).days
    return age_in_days * 24 * 60


def convert_to_words(number):
    return num2words(number).replace(",", "")


if __name__ == "__main__":
    main()
