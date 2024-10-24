# Main function to calculate the tip based on the meal price and desired tip percentage
def main():
    dollars = dollars_to_float(input("How much was the meal? "))
    percent = percent_to_float(input("What percentage would you like to tip? "))
    tip = dollars * percent
    print(f"Leave ${tip:.2f}") # Print the tip amount formatted to 2 decimal places

# Convert dollar string to float
def dollars_to_float(d):
    amount = float(d.strip("$")) # Remove the dollar sign and convert to float
    return amount

# Convert percentage string to float
def percent_to_float(p):
    percentage = float(p.strip("%")) / 100 # Remove the percentage sign, convert to float and divide by 100
    return percentage

# Execute the main function
main()