def calculate_energy(mass):
    c_square = 89875517873681764  # Speed of light squared in m^2/s^2
    energy = mass * c_square  # Calculate the energy
    return energy


def main():
    mass = int(input("Enter the mass in kg: "))
    energy = calculate_energy(mass)
    print("Equivelant energy (in Joules):", energy)


if __name__ == "__main__":
    main()
