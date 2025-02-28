import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare

def exponential_goodness_of_fit(n=100, mean=0.5, bin_width=0.25, max_range=3.0, seed=0):
    """
    Generates `n` Exponential(mean=mean) random values,
    bins them from 0..max_range plus one final bin [max_range, infinity),
    computes observed vs expected frequencies, and performs a chi-square test.
    """
    np.random.seed(seed)
    
    # Rate = 1/mean
    lam = 1.0 / mean
    
    # Generate data
    data = np.random.exponential(scale=mean, size=n)
    
    # Define bin edges
    edges = np.arange(0, max_range, bin_width)
    edges = np.append(edges, [np.inf])  # ensures total sum is exactly n
    
    # Observed frequencies
    observed, bin_edges = np.histogram(data, bins=edges)
    
    # Expected frequencies
    expected = []
    for i in range(len(edges) - 1):
        a = edges[i]
        b = edges[i + 1]
        if np.isinf(b):
            # Probability X >= a
            p_bin = np.exp(-lam * a)
        else:
            # Probability a <= X < b = F(b) - F(a)
            p_bin = (1 - np.exp(-lam * b)) - (1 - np.exp(-lam * a))
        expected.append(n * p_bin)
    
    # Chi-square test
    chi_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
    
    # Plot
    plt.figure(figsize=(8,4))
    # For plotting, omit the infinity edge (edges[:-1])
    plt.hist(data, bins=edges[:-1], alpha=0.7, edgecolor='black')
    plt.title(f"Histogram of {n} Exponential(Mean={mean}) Values")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.show()
    
    # Print results
    print("Observed:", observed)
    print("Expected:", np.round(expected, 2))
    print(f"Chi-square Statistic: {chi_stat:.4f}")
    print(f"p-value: {p_value:.4f}")
    
    return observed, expected, chi_stat, p_value

if __name__ == "__main__":
    observed, expected, chi_stat, p_value = exponential_goodness_of_fit(
        n=100, mean=0.5, bin_width=0.25, max_range=3.0, seed=42
    )