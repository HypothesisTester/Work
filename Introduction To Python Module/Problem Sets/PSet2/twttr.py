text = input("Enter tweet: ")  # Get tweet from user
output = ""

# Remove vowels from tweet
for character in text:
    if character.lower() not in {"a", "e", "i", "o", "u"}:
        output += character

print(output)  # Output tweet without vowels