from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = defaultdict(list) # mapping charCount to list of Anagrams
    
        for s in strs:
            count = [0] * 26 # a ... z
            
            for c in s:
                count[ard(c) - ard("a")] += 1
                
            result[tuple(count)].append(s)
        
        return result.values()