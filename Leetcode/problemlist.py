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
        c = a+b
        a, b = b, c
    return c

# Or

class Solution:
    def fib(self, n: int) -> int:
        if n == 0 or n == 1:
             return n
        
        dp = [0 for _ in range(n + 1)]

        dp[0] = 0
        dp[1] = 1
        
        for i in range(2, n + 1):
            
            dp[i] = dp[i - 1] + dp[i - 2]
            
        
