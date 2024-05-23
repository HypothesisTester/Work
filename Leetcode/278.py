def firstBadVersion(self, n):
        i = 1
        j = n
        while (i < j):
                pivot = (i+j) // 2
                if (isBadVersion(pivot)):
                        