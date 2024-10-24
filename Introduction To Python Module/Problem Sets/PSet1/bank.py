def bank():
    user_greeting = input("Enter your greeting: ")  # Get greeting from user
    user_greeting = user_greeting.lstrip()  # Remove leading whitespaces
    user_greeting_lower = user_greeting.lower()  # Convert to lowercase

    # Determine output based on greeting prefix
    if user_greeting_lower.startswith("hello"):
        print("$0")
    elif user_greeting_lower.startswith("h"):
        print("$20")
    else:
        print("$100")

bank()  # Run bank function