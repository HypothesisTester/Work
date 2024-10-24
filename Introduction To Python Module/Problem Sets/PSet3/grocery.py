def main():
    grocery_list = {}

    while True:
        try:
            item = input("Enter an item: ")
        except EOFError:
            break

        item = item.lower()

        # Update item count in the grocery_list dictionary
        if item in grocery_list:
            grocery_list[item] += 1
        else:
            grocery_list[item] = 1

    sorted_list = sorted(grocery_list.items())

    for item, count in sorted_list:
        print(f"{count} {item.upper()}")


if __name__ == "__main__":
    main()
