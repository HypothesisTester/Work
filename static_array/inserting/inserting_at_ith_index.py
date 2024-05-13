# Insert n into index i after shifting elements to the right.
# Assuming i is a valid index and arr is not full.
def insertMiddle(arr, i, n, length):
     # Shift starting from the end to i.
     for index in range(length - 1, i - 1, -1):
          arr[index + 1] = arr[index]
          
     # Insert at i
     arr[i] = n