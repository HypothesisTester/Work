import numpy as np

def dp(x, y):
    # states: 0=R1, 1=R2, 2=U1, 3=U2
    dp = np.zeros((x + 1, y + 1, 4), dtype=int)

    # edge starts (can make at most 2 in a row along an axis)
    if x >= 1: dp[1, 0, 0] = 1
    if x >= 2: dp[2, 0, 1] = 1
    if y >= 1: dp[0, 1, 2] = 1
    if y >= 2: dp[0, 2, 3] = 1

    for i in range(1, x + 1):
        for j in range(1, y + 1):
            dp[i, j, 0] = dp[i - 1, j, 2] + dp[i - 1, j, 3]  # end with R1
            dp[i, j, 1] = dp[i - 1, j, 0]                    # end with R2
            dp[i, j, 2] = dp[i, j - 1, 0] + dp[i, j - 1, 1]  # end with U1
            dp[i, j, 3] = dp[i, j - 1, 2]                    # end with U2

    return int(dp[x, y].sum())

print(dp(5, 6))  # -> 113
print(dp(7, 4))  # -> 30