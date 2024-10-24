def main():
    while True:
        try:
            fraction = input("Enter fraction (X/Y): ")
            numerator, denominator = fraction.split("/")
            numerator = int(numerator)
            denominator = int(denominator)

            if (
                not isinstance(numerator, int)
                or not isinstance(denominator, int)
                or denominator == 0
            ):
                raise ValueError

            fuel_percentage = round((numerator / denominator) * 100)

            if fuel_percentage <= 1:
                print("E")
            elif fuel_percentage >= 99:
                print("F")
            else:
                print(f"{fuel_percentage}%")

            break

        except (ValueError, ZeroDivisionError):
            print("Invalid fraction. Please try again.")


if __name__ == "__main__":
    main()
