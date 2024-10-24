def main():
    text = str(input("Enter tweet: "))
    print(shorten(text))


def shorten(word):
    output = ""
    for character in word:
        if character.lower() not in {"a", "e", "i", "o", "u"}:
            output += character # Add consonants to output

    return output


if __name__ == "__main__":
    main()
