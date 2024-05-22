# The guess API is already defined for you.
# @param num, your guess
# @return -1 if num is higher than the picked number
#          1 if num is lower than the picked number
#          otherwise return 0
# def guess(num: int) -> int:

class Solution:
    def guessNumber(self, n: int) -> int:
        lowerBound, upperBound = 1, n
        # Binary division faster than (lowerBound + upperBound) //2
        myGuess = (lowerBound+upperBound) >> 1
        # walrus operator ':=' - assigns value of the function to the variable 'res'
        # and then compare res with 0
        while (res := guess(myGuess)) != 0:
            if res == 1:
                lowerBound = myGuess+1
            else:
                upperBound = myGuess-1
            myGuess = (lowerBound+upperBound) >> 1
        
        return myGuess
    
# Or

def guessNumber(self, n: int) -> int:
	low = 0
	high = n
	while low <= high:
            mid = (low + high ) // 2
            res = guess(mid)
            if res < 0:
			    high = mid - 1
            
            elif res > 0:
			    low = mid + 1
        
            else:
                return mid
            
            
class Solution:
    def guessNumber(self, n: int) -> int:
        low = 1
        high = n
        
        while low<=high:
            mid = (low+high)//2
            gussed = guess(mid)
            
            if gussed == 0:
                return mid
            if gussed<0:
                high = mid-1
            else:
                low = mid+1
        
        return low
            

class Solution:
    def guessNumber(self, n: int) -> int:
        left,right=0,n+1
        while left<=right:
               mid=left+(right-left)//2
            if guess(mid)==0:
                return mid
            if guess(mid)==1:
                left=mid+1
            else:
                right=mid-1
        
            
            