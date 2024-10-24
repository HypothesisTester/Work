# Function to convert specific substrings (emoticons) to their emoji counterparts
def convert(input_string):
    converted_string = input_string.replace(":)", "🙂").replace(":(", "🙁")
    return converted_string


def main():
    input_text = input("Enter your text: ")
    converted_text = convert(input_text)
    print("Converted text:", converted_text)


if __name__ == "__main__":
    main()
