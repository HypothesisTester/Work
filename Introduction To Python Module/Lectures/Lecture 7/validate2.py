import re

email = input("What's your email? ").strip()

# Instead of '.+' ..* also works in the same fashion
if re.search(r"^[^@]+@[^@]+\.edu$", email):
    print("valid")
else:
    print("Invalid")