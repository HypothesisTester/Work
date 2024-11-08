import matplotlib.pyplot as plt
import numpy as np

def find_intersection(coeff1, const1, coeff2, const2):
    """
    Finds the intersection point of two lines.
    Returns (x, y) if a unique solution exists, else None.
    """
    A = np.array([coeff1, coeff2])
    B = np.array([const1, const2])
    try:
        solution = np.linalg.solve(A, B)
        return tuple(solution)
    except np.linalg.LinAlgError:
        return None

def is_feasible(point, constraints):
    """
    Checks if a point satisfies all given constraints.
    """
    x, y = point
    for constraint in constraints:
        lhs = constraint['coefficients'][0]*x + constraint['coefficients'][1]*y
        if constraint['type'] == '>=' and lhs < constraint['constant']:
            return False
        elif constraint['type'] == '<=' and lhs > constraint['constant']:
            return False
        elif constraint['type'] == '=' and not np.isclose(lhs, constraint['constant']):
            return False
    return True

def plot_constraints(x1, caloric_x2, protein_x2, budget_x2):
    """
    Plots constraints and shades feasible regions.
    """
    plt.figure(figsize=(10, 8))
    plt.plot(x1, caloric_x2, label='Caloric Constraint', color='red')
    plt.fill_between(x1, caloric_x2, 50, where=(caloric_x2 < 50), color='red', alpha=0.3)
    plt.plot(x1, protein_x2, label='Protein Constraint', color='green')
    plt.fill_between(x1, protein_x2, 50, where=(protein_x2 < 50), color='green', alpha=0.3)
    plt.plot(x1, budget_x2, label='Budget Constraint', color='blue')
    plt.fill_between(x1, 0, budget_x2, where=(budget_x2 > 0), color='blue', alpha=0.3)
    plt.xlim(0, 15)
    plt.ylim(0, 50)
    plt.xlabel('Brown Rice Servings (x₁)')
    plt.ylabel('Chicken Breast Fillet Servings (x₂)')
    plt.title('Feasible Region for Diet Problem')
    plt.legend(loc='upper right')
    plt.grid(True)
    return plt

def main():
    x1 = np.linspace(0, 20, 400)
    caloric_x2 = (3092 - 223 * x1) / 108
    protein_x2 = (56 - 5.1 * x1) / 23
    budget_x2 = (20 - 0.074 * x1) / 0.774
    plt = plot_constraints(x1, caloric_x2, protein_x2, budget_x2)
    
    constraints = [
        {'type': '>=', 'coefficients': [223, 108], 'constant': 3092},
        {'type': '>=', 'coefficients': [5.1, 23], 'constant': 56},
        {'type': '<=', 'coefficients': [0.074, 0.774], 'constant': 20}
    ]
    
    intersection1 = find_intersection([223, 108], 3092, [5.1, 23], 56)
    intersection2 = find_intersection([223, 108], 3092, [0.074, 0.774], 20)
    intersection3 = find_intersection([5.1, 23], 56, [0.074, 0.774], 20)
    
    intersections = []
    labels = []
    
    if intersection1 and is_feasible(intersection1, constraints):
        intersections.append(intersection1)
        labels.append('Intersection Caloric & Protein')
    if intersection2 and is_feasible(intersection2, constraints):
        intersections.append(intersection2)
        labels.append('Intersection Caloric & Budget')
    if intersection3 and is_feasible(intersection3, constraints):
        intersections.append(intersection3)
        labels.append('Intersection Protein & Budget')
    
    print("=== Intersection Points ===")
    for i, point in enumerate(intersections):
        print(f"{labels[i]}: x₁ = {point[0]:.2f}, x₂ = {point[1]:.2f}")
    if not intersections:
        print("No feasible intersection points found.")
        return
    
    def objective(x1, x2):
        return 0.074 * x1 + 0.774 * x2
    
    costs = [objective(point[0], point[1]) for point in intersections]
    for i, cost in enumerate(costs):
        print(f"Cost at {labels[i]}: €{cost:.2f}")
    
    min_cost_index = np.argmin(costs)
    optimal_point = intersections[min_cost_index]
    print("\n=== Optimal Solution ===")
    print(f"Optimal Point: x₁ = {optimal_point[0]:.2f}, x₂ = {optimal_point[1]:.2f}")
    print(f"Minimum Cost: €{costs[min_cost_index]:.2f}")
    
    for i, point in enumerate(intersections):
        plt.plot(point[0], point[1], 'o', label=f"{labels[i]} (Cost: €{costs[i]:.2f})")
        plt.annotate(f"({point[0]:.2f}, {point[1]:.2f})", (point[0], point[1]),
                     textcoords="offset points", xytext=(10,10), ha='center')
    
    plt.plot(optimal_point[0], optimal_point[1], 'ro', markersize=10, label='Optimal Solution')
    plt.annotate(f"Optimal\n({optimal_point[0]:.2f}, {optimal_point[1]:.2f})",
                 (optimal_point[0], optimal_point[1]), xytext=(10,-15), ha='center', color='red',
                 fontsize=12, fontweight='bold')
    plt.legend(loc='upper right')
    plt.savefig('diet_problem_with_optimal.png')
    print("\nThe plot with intersection points and the optimal solution has been saved.")

if __name__ == "__main__":
    main()