def main():
    student = get_student()
    if student[0] == "Padma":
        student[1] == "Ravenclaw"
    print(f"{student[0]} from {student[1]}")

def get_student():
    name = input("Name: ")
    house = input("House: ")
    # if return [name, house] then treated as list and then has mutability (values can be changed)
    return (name, house)

if __name__ == "__main__":
    main()