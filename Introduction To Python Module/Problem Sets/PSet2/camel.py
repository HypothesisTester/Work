def main():
    variable = input("Enter camel case variable: ")
    snake_case_variable = convert_to_snake_case(variable)
    print(snake_case_variable)


def convert_to_snake_case(variable):
    for i in range(len(variable)):
        if variable[i].isupper():
            variable = variable[:i] + "_" + variable[i].lower() + variable[i + 1 :]
    return variable


if __name__ == "__main__":
    main()
