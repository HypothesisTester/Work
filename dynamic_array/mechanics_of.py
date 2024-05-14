# Insert n in the last position of the array
def pushback(self, n):
    if self.length == self.capacity:
        self.resize()
    
    # insert at next empty position
    self.arr[self.length] = n
    self.length += 1