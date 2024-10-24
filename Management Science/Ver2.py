# diet_problem_enhanced.py

import matplotlib.pyplot as plt
import numpy as np

def find_intersection(coeff1, const1, coeff2, const2):
    """
    Finds the intersection point of two lines given by:
    coeff1[0]*x + coeff1[1]*y = const1
    coeff2[0]*x + coeff2[1]*y = const2
    Returns (x, y) if there is a unique solution, else None.
    """
    A = np.array([coeff1, coeff2])
    B = np.array([const1, const2])
    try:
        solution = np.linalg.solve(A, B)
        return tuple(solution)
    except np.linalg.LinAlgError:
        # Lines are parallel or coincident
        return None

def is_feasible(point, constraints):
    """
    Checks if a point satisfies all constraints.
    Constraints is a list of dictionaries with:
    - 'type': '>=', '<=', or '='
    - 'coefficients': [a, b] for ax + by
    - 'constant': value on the other side
    """
    x, y = point
    for constraint in constraints:
        lhs = constraint['coefficients'][0]*x + constraint['coefficients'][1]*y
        if constraint['type'] == '>=':
            if lhs < constraint['constant']:
                return False
        elif constraint['type'] == '<=':
            if lhs > constraint['constant']:
                return False
        elif constraint['type'] == '=':
            if not np.isclose(lhs, constraint['constant']):
                return False
    return True

def plot_constraints(x1, caloric_x2, protein_x2, budget_x2):
    """
    Plots the constraints and shades the feasible region.
    """
    plt.figure(figsize=(10, 8))
    
    # Caloric constraint
    plt.plot(x1, caloric_x2, label='Caloric Constraint: 223x₁ + 108x₂ ≥ 3092', color='red')
    plt.fill_between(x1, caloric_x2, 50, where=(caloric_x2 < 50), color='red', alpha=0.3)
    
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
    
    return plt

def main():
    # Define the range for x1
    x1 = np.linspace(0, 20, 400)
    
    # Define the constraints
    # Caloric constraint: 223x1 + 108x2 >= 3092 => x2 >= (3092 - 223x1)/108
    caloric_x2 = (3092 - 223 * x1) / 108
    
    # Protein constraint: 5.1x1 + 23x2 >= 56 => x2 >= (56 - 5.1x1)/23
    protein_x2 = (56 - 5.1 * x1) / 23
    
    # Budget constraint: 0.074x1 + 0.774x2 <= 10 => x2 <= (10 - 0.074x1)/0.774
    budget_x2 = (10 - 0.074 * x1) / 0.774
    
    # Plot the constraints
    plt = plot_constraints(x1, caloric_x2, protein_x2, budget_x2)
    
    # Define the constraints for feasibility checking
    constraints = [
        {'type': '>=', 'coefficients': [223, 108], 'constant': 3092},   # Caloric
        {'type': '>=', 'coefficients': [5.1, 23], 'constant': 56},     # Protein
        {'type': '<=', 'coefficients': [0.074, 0.774], 'constant': 10} # Budget
    ]
    
    # Define the equations for intersection
    # 1. Caloric and Protein
    intersection1 = find_intersection([223, 108], 3092, [5.1, 23], 56)
    
    # 2. Caloric and Budget
    intersection2 = find_intersection([223, 108], 3092, [0.074, 0.774], 10)
    
    # 3. Protein and Budget
    intersection3 = find_intersection([5.1, 23], 56, [0.074, 0.774], 10)
    
    # List of intersection points
    intersections = []
    labels = []
    
    # Check each intersection for feasibility
    if intersection1:
        if is_feasible(intersection1, constraints):
            intersections.append(intersection1)
            labels.append('Intersection Caloric & Protein')
    
    if intersection2:
        if is_feasible(intersection2, constraints):
            intersections.append(intersection2)
            labels.append('Intersection Caloric & Budget')
    
    if intersection3:
        if is_feasible(intersection3, constraints):
            intersections.append(intersection3)
            labels.append('Intersection Protein & Budget')
    
    # Print the intersection points
    print("=== Intersection Points ===")
    for i, point in enumerate(intersections):
        print(f"{labels[i]}: x₁ = {point[0]:.2f}, x₂ = {point[1]:.2f}")
    
    # If no feasible intersection points, notify the user
    if not intersections:
        print("No feasible intersection points found.")
        return
    
    # Define the objective function coefficients
    # Z = 0.074x1 + 0.774x2
    def objective(x1, x2):
        return 0.074 * x1 + 0.774 * x2
    
    # Evaluate the objective function at each feasible intersection
    costs = []
    for point in intersections:
        cost = objective(point[0], point[1])
        costs.append(cost)
        print(f"Cost at {labels[intersections.index(point)]}: €{cost:.2f}")
    
    # Determine the optimal solution (minimum cost)
    min_cost_index = np.argmin(costs)
    optimal_point = intersections[min_cost_index]
    optimal_label = labels[min_cost_index]
    optimal_cost = costs[min_cost_index]
    
    print("\n=== Optimal Solution ===")
    print(f"Optimal Point: x₁ = {optimal_point[0]:.2f}, x₂ = {optimal_point[1]:.2f}")
    print(f"Minimum Cost: €{optimal_cost:.2f}")
    
    # Plot the intersection points
    for i, point in enumerate(intersections):
        plt.plot(point[0], point[1], 'o', label=f"{labels[i]} (Cost: €{costs[i]:.2f})")
        plt.annotate(f"({point[0]:.2f}, {point[1]:.2f})", (point[0], point[1]),
                     textcoords="offset points", xytext=(10,10), ha='center')
    
    # Highlight the optimal point
    plt.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label='Optimal Solution')
    plt.annotate(f"Optimal\n({optimal_point[0]:.2f}, {optimal_point[1]:.2f})",
                 (optimal_point[0], optimal_point[1]),
                 textcoords="offset points", xytext=(10,-15), ha='center', color='red',
                 fontsize=12, fontweight='bold')
    
    # Update the legend to include new points
    plt.legend(loc='upper right')
    
    # Save the updated plot as an image file
    plt.savefig('diet_problem_with_optimal.png')
    
    # Show the plot (optional, since you might run this in a terminal)
    # plt.show()
    
    print("\nThe plot with intersection points and the optimal solution has been saved as 'diet_problem_with_optimal.png'.")

if __name__ == "__main__":
    main()