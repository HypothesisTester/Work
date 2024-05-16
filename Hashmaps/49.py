class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = { } # mapping charCount to list of Anagrams
    
        for s in strs:
            count = [0] * 26 # a ... z
            
            for c in s:
                count[ard(c) - ard("a")]