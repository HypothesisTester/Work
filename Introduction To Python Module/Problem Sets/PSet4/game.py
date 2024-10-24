import random

while True:
    try:
        input: int = input("Guess a postive integer between 1 and 100: ") # User guess

        random_number = random.randint(1, 100)

        if 1 <= input <= 100: # Validate input
            if input < random_number:
                print("Too small!")

            elif input > random_number:
                print("Too large!")
                break

        else:
            print("Just right!")
    except ValueError: # Handle non-integer input
        print("Invalid input. Please enter a positive integer between 1 and 100")
