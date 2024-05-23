def firstBadVersion(self, n):
    i = 1
    j = n
    while (i < j):
        pivot = (i+j) // 2
        if (isBadVersion(pivot)):
            j = pivot       # keep track of the leftmost bad version
        else:
            i = pivot + 1   # the one after the rightmost good version
    return i   

# Or

class Solution:
	def firstBadVersion(self, n: int) -> int:
        
        result = 1
        start, end = 1, n
             
         while start <= end:
                
                mid = (start + end) // 2
                  
                if isBadVersion(mid) == False:
                    start = mid + 1
                                
                else:
                    end = mid - 1
                    result = mid
                       
		return result