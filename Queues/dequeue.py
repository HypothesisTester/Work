def dequeue(self):
    # Queue is empty
    if not self.left:
        return None
    
    # Remove left node and return value
    val = self.left.val
    self.left = self.left.next
    if not self.left:
        self.right = None
    return val