class Solution:
    def fib(self, n: int) -> int:
        a, b = 0, 1
        for i in range(N): a, b = b, a + b
        return a
    
# Or

def fib(self, N: int) -> int:
    if N < 2: return N
    a, b = 0, 1
    for _ in range(N-1):
        