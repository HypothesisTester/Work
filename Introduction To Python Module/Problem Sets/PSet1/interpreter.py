def calculate_expression(x, operator, z):
    # Calculate result based on operator
    if operator == "+":
        return x + z
    elif operator == "-":
        return x - z
    elif operator == "*":
        return x * z
    elif operator == "/":
        return x / z


def main():
    # Get expression from user
    expression = input("Enter an arithmetic expression (x y z): ")
    x, operator, z = expression.split()

    # Convert to integers
    x = int(x)
    z = int(z)

    # Calculate and format result
    result = calculate_expression(x, operator, z)
    formatted_result = "{:.1f}".format(result)
    print("Result:", formatted_result)


if __name__ == "__main__":
    main()
