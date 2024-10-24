import sys

names = []

while True:
    try:
        name = input("Name: ").title()

        if not name:
            break

        names.append(name)

    except EOFError:  # Handle end-of-file (Ctrl-D)
        farewell = "Adieu, adieu, to "

        # Generate farewell message based on number of names
        if len(names) == 1:
            farewell += names[0]
        else:
            farewell += ", ".join(names[:-1]) + f", and {names[-1]}"

        print(farewell)
        sys.exit(0)
