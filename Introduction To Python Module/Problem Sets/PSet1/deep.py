def answer_question(input):
    # Check if input matches known answers for the Great Question
    if input == "42" or input == "forty-two" or input == "forty two":
        print("Yes")
    else:
        print("No")

def main():
    question_life = input("What's the answer to the Great Question of life: ")  # Get user input
    answer_question(question_life)  # Evaluate answer

main()