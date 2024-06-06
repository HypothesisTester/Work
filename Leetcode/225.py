from collections import deque

class MyStack:

    def __init__(self):
        # Initialize an empty deque to simulate stack operations
        self.q = deque()

    def push(self, x: int) -> None:
        # Append the element to the end of the deque
        self.q.append(x)
        

    def pop(self) -> int:
        # Rotate the deque to simulate stack pop operation
        # Move all elements except the last one to the front of the deque
        for _ in range(len(self.q) - 1):
            self.push(self.q.popleft())
        # Pop the last element which is now at the fron
        return self.q.popleft()

    def top(self) -> int:
        return self.q[-1]
        

    def empty(self) -> bool:
        return len(self.q) == 0
        


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()