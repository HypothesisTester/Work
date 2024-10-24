import random
import sys


def main():
    level = get_level()  # Get difficulty level from user
    score = 0 # Initialize score

    for _ in range(10): # 10 rounds
        x = generate_integer(level)
        y = generate_integer(level)
        answeer = x + y # Correct answer
        problem = f"{x} + {y} = "  # Problem to be shown

        for _ in range(3): # Three attempts for each problem
            user_input = input(problem)
            try:
                user_answer = int(user_input)
                if user_answer == answer:
                    score += 1 # Increase score
                    break
                else:
                    print("EEE")
            except ValueError:
                print("EEE")
        else:
            print(f"Your score: {score} is: {answer}")
    print(f"Your score: {score} out of 10")


def get_level():
    while True:
        level = input("Enter the level (1, 2, or 3): ")
        if level in ["1", "2", "3"]:
            return int(level)
        else:
            print("Invalid level. Please enter 1, 2 or 3.")


def generate_integer(level):
    # Generate integers based on level
    if level == 1:
        return random.randint(0, 9)
    elif level == 2:
        return random.randint(0, 99)
    elif level == 3:
        return random.randint(0, 9992)
    else:
        raise ValueError("Invalid level")


if __name__ == "__main__":
    main()
