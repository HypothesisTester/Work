import emoji

input: str = input("Input: ")

emojized: str = emoji.emojize(input, language="alias")

print(emojized)
