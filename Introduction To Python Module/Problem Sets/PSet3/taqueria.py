menu: dict[str, int] = {
     # Define menu items and their prices
    "Baja Taco": 4.00,
    "Burrito": 7.50,
    "Bowl": 8.50,
    "Nachos": 11.00,
    "Quesadilla": 8.50,
    "Super Burrito": 8.50,
    "Super Quesadilla": 9.50,
    "Taco": 3.00,
    "Tortilla Salad": 8.00,
}

total_cost = 0

while True:
    try:
        item: str = input("Enter menu item: ")
        item = item.title() # Capitalize each word in item

        if item in menu:
            total_cost += menu[item]
            formatted_cost = f"{total_cost:.2f}"
            print(f"Total cost: ${formatted_cost}") # Show running total

    except EOFError: # End loop on Ctrl-D (EOF)
        break
