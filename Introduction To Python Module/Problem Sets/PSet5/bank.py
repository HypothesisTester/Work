def main():
    user_greeting = input("Enter your greeting: ")
    user_greeting = user_greeting.strip().lower

    result = value(user_greeting)
    print(result)


def value(greeting):
    if greeting.startswith("hello"):
        return "$0"
    elif greeting.startswith("h"):
        return "$20"
    else:
        return "$100"


if __name__ == "__main__":
    main()
