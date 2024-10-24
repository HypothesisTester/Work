import matplotlib.pyplot as plt
import numpy as np

# Define the range for x1
x1 = np.linspace(0, 20, 400)

# Caloric constraint: 223x1 + 108x2 >= 3092 => x2 >= (3092 - 223x1)/108
caloric_x2 = (3092 - 223 * x1) / 108

# Protein constraint: 5.1x1 + 23x2 >= 56 => x2 >= (56 - 5.1x1)/23
protein_x2 = (56 - 5.1 * x1) / 23

# Budget constraint: 0.074x1 + 0.774x2 <= 10 => x2 <= (10 - 0.074x1)/0.774
budget_x2 = (10 - 0.074 * x1) / 0.774

# Plot the constraints
plt.figure(figsize=(10, 8))

# Caloric constraint
plt.plot(x1, caloric_x2, label='Caloric Constraint: 223x₁ + 108x₂ ≥ 3092', color='red')
plt.fill_between(x1, caloric_x2, 50, where=(caloric_x2 < 50), color='red', alpha=0.6)

# Protein constraint
plt.plot(x1, protein_x2, label='Protein Constraint: 5.1x₁ + 23x₂ ≥ 56', color='green')
plt.fill_between(x1, protein_x2, 50, where=(protein_x2 < 50), color='green', alpha=0.3)

# Budget constraint
plt.plot(x1, budget_x2, label='Budget Constraint: 0.074x₁ + 0.774x₂ ≤ 10', color='blue')
plt.fill_between(x1, 0, budget_x2, where=(budget_x2 > 0), color='blue', alpha=0.3)

# Feasible region boundaries
plt.xlim(0, 15)
plt.ylim(0, 50)

# Labels and title
plt.xlabel('Brown Rice Servings (x₁)')
plt.ylabel('Chicken Breast Fillet Servings (x₂)')
plt.title('Feasible Region for Simplified Diet Problem')

# Adding legend
plt.legend(loc='upper right')

# Adding grid
plt.grid(True)

# Save the plot as an image file
plt.savefig('diet_problem.png')

# Show the plot (optional, since you might run this in a terminal)
# plt.show()

print("The plot has been saved as 'diet_problem.png'.")