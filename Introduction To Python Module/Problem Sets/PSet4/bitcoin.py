import requests
import sys

# Validate command-line argument
def check():
    if len(sys.argv) != 2:
        sys.exit("Missing command-line argument")

    try:
        float(sys.argv[1])
    except ValueError:
        sys.exit("Command-line arguemnt is not a number")

try:
    check()
    r = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")  # Fetch Bitcoin price
    rate: float = r.json()["bpi"]["USD"]["rate_float"]
    per_coin = rate * float(sys.argv[1])
    print(f"${per_coin:,.4f}")

except requests.RequestException:
    sys.exit("Error: Unable to reach CoinDesk API.") # Handle API request exception
