import validators


def get_email():
    email_address = input("Please enter an email address: ")
    return email_address


def validate_email(email):
    # Use the 'validators' library to check if the email is valid
    if validators.email(email):
        print("Valid")
    else:
        print("Invalid")


def main():
    email_address = get_email()
    validate_email(email_address)


if __name__ == "__main__":
    main()
