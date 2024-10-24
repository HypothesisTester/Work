import re
import sys


def main():
    print(count(input("Text: ")))


def count(s):
    # '\b' denotes word boundaries
    # len(re.findall()) returns count of 'um' occurrences
    return len(re.findall(r"\bum\b", s , re.IGNORECASE))


if __name__ == "__main__":
    main()
