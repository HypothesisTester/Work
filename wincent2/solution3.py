#!/usr/bin/env python3
"""
Politics   –  expected number of days until consensus
"""

import sys
from math import inf

def solve_case(n: int, k: int, p: int) -> float | int:
    """
    Return E[T] or -1 if the expectation is infinite.
    """
    if n == 1:                    # already unanimous
        return 0.0
    if p == 0:                    # nobody ever converts
        return -1
    q = p / 100.0
    return 2.0 * (n - 1) ** 2 / (k * (k + 1) * q)

# ----------------------------------------------------------------------

def main() -> None:
    it = iter(sys.stdin.read().strip().split())
    t  = int(next(it))
    out_lines = []
    for _ in range(t):
        n = int(next(it))
        k = int(next(it))
        p = int(next(it))
        S = [next(it) for _ in range(n)]   # S[i] are irrelevant for E[T]
        ans = solve_case(n, k, p)
        out_lines.append("-1" if ans == -1 else f"{ans:.12f}")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()