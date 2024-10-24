# Insert n in the last position of the array
def pushback(self, n):
    if self.length == self.capacity:
        self.resize()
    
    # insert at next empty position
    self.arr[self.length] = n
    self.length += 1

def resize(self):
    # Create new array of double capacity
    self.capacity = 2 * self.capacity
    newArr = [0] * self.capacity
    
    # Copy elements to newArr
    for i in range(self.length):
        newArr[i] = self.arr[i]
    self.arr = newArr