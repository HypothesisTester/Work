def main():
    plate = input("Plate: ")  # Get license plate from user
    if is_valid(plate):  # Check if valid
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if len(s) < 2 or len(s) > 6:  # Check length
        return False

    if not s[:2].isalpha():  # Check first two characters are alphabets
        return False

    prohibited_characters = {".", " ", "!"}  # Set of prohibited characters
    for char in s:  # Check for prohibited characters
        if char in prohibited_characters:
            return False

    for char in s[1:-1]:  # Check middle characters aren't digits
        if char.isdigit():
            return False

    if s[0] == "0":  # Check first character isn't '0'
        return False

    else:
        return True  # If all checks pass, it's valid


main()  