def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    if len(s) < 2 or len(s) > 6:
        return False

    if not s[:2].isalpha(): # First two characters must be alphabets
        return False

    prohibited_characters = {".", " ", "!"}
    for char in s:
        if char in prohibited_characters:
            return False

    for char in s[1:-1]:
        if char.isdigit(): # Check if any character except first is a digit
            return False

    if s[0] == "0":
        return False

    else:
        return True


if __name__ == "__main__":
    main()
