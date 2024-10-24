from pyfiglet import Figlet
import sys

# Check for correct number of command-line arguments
if len(sys.argv) != 3:
    sys.exit("Invalid usage")

# Validate command-line option
if sys.argv[1] not in ["-f", "-font"]:
    sys.exit("Invalid usage")

input: str = input("Input: ")

figlet = Figlet()
figlet.getFonts() # Retrieve available fonts

figlet.setFont(font=sys.argv[2]) # Set font based on command-line argument

print(figlet.renderText(input))
