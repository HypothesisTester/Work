# This is a placeholder for the isBadVersion API. In practice, this would be provided.
def isBadVersion(version: int) -> bool:
    pass  # Placeholder implementation

class Solution:
    def firstBadVersion(self, n: int) -> int:
        start, end = 1, n
        result = -1  # Initialize result to -1 to indicate no bad version found (optional)
        
        while start <= end:
            mid = (start + end) // 2
            
            if not isBadVersion(mid):
                start = mid + 1
            else:
                end = mid - 1
                result = mid
        
        return result
