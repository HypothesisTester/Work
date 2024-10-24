def main():
    while True:
        try:
            fraction = input("Enter fraction(X/Y): ")
            percentage = convert(fraction)
            fuel_gauge = gauge(percentage)
            print(fuel_gauge)
            break
        except (ValueError, ZeroDivisionError) as e:
            print(str(e))

# Function to convert a fraction to percentage
def convert(fraction):
    try:
        numerator, denominator = fraction.split("/")
        numerator = int(numerator)
        denominator = int(denominator)
    except ValueError:
        raise ValueError(
            "Invalid input. Expected format is 'X/Y' where X and Y are integers."
        )

    if numerator > denominator:
        raise ValueError("Numerator cannot be greater than denominator.")
    if denominator == 0:
        raise ZeroDivisionError("Denominator cannot be zero.")

    percentage = round((numerator / denominator) * 100)
    return percentage

# Function to interpret the percentage as a fuel gauge
def gauge(percentage):
    # Handle edge cases for empty and full gauge
    if percentage <= 1:
        return "E"
    elif percentage >= 99:
        return "F"
    else:
        return f"{percentage}%"


if __name__ == "__main__":
    main()
