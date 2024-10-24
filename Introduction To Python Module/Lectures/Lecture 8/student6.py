class Student:
    def __init__(self, name, house, patronus):
        if not name:
            raise ValueError("Missing name")
        if house not in ["Gryffindor", "Hufflepuff", "Hufflepuff", "Ravenclaw", "Slytherin"]:
            raise ValueError("Invalid house")
        self.name = name
        self.house = house
        self.patronus = patronus

    def __str__(self):
        return f"{self.name} from {self.house}"

def charm(self):
    if self.patronus == "Stag":
        return "Insert horse emoji"
    elif self.patronus == "Otter":
        return "Insert Otter emoji"
    elif self.patronus == "Jack Russell terrier":
        return "Insert dog emoji"
    else:
        return "Insert magic wand emoji"


def main():
    student = get_student()
    print("Expecto Patronum!")
    print(student.charm())


def get_student():
   name = input("Name: ")
   house = input("House: ")
   patronus = input("Patronus: ")
   return Student(name, house, patronus)


if __name__ == "__main__":
    main()