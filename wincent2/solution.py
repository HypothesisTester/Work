#!/usr/bin/env python3
import sys
from math import ceil

def min_regularity(counts, n):
    """
    Find the smallest r in [1..n] for which we can form a period-r string
    using exactly the counts[i] copies of each letter.
    We check the classic necessary+sufficient “block‐cover” inequalities:
        sum ceil(c_i / ceil(n/r)) <= r <= sum floor(c_i / floor(n/r))
    """
    freqs = [c for c in counts if c>0]
    for r in range(1, n+1):
        big = ceil(n / r)
        small = big - 1
        tmin = sum((c + big - 1)//big for c in freqs)
        # if small==0, floor(c/small) is ∞ in effect – we only need the left
        if small>0:
            tmax = sum(c//small for c in freqs)
            if not (tmin <= r <= tmax):
                continue
        else:
            # small==0 ⇒ all c must fit into blocks of size big only
            if tmin > r:
                continue
        return r
    return n

def min_moves_for_r(positions, n, r):
    """
    Given the initial positions of each letter (positions[ch] = sorted list of indices),
    build *any* period-r string T that uses exactly those letters, then compute
    the minimal total number of single‐step moves (sum |i-j|) to go from S→T.
    """
    # 1) compute the class sizes f[j]
    f = [ ((n-1-j)//r + 1) for j in range(r) ]
    k = n % r         # number of classes of size big = ceil(n/r)
    big = (n + r - 1)//r
    small = big - 1

    # 2) for each letter ch determine how many classes it needs in total *t[ch]*
    #    and among them exactly *x[ch]* big‐classes
    t = {}
    x = {}
    for ch, lst in positions.items():
        c = len(lst)
        # t[ch] = minimal number of classes needed if all were size=big
        tc = (c + big - 1)//big
        t[ch] = tc
        # if it uses tc classes,   c = x*big + (tc-x)*small   ⇒ x = c - tc*small
        x[ch] = c - tc*small

    # 3) collect class‐indices by size, along with their “center” for cost
    big_classes   = []
    small_classes = []
    for j in range(r):
        sz = f[j]
        # the actual indices in class j are j, j+r, j+2r, ...
        first = j
        last  = j + (sz-1)*r
        center = (first + last) / 2.0
        if sz == big:
            big_classes.append((center, j))
        else:
            small_classes.append((center, j))
    big_classes.sort()
    small_classes.sort()

    # 4) assign classes greedily by ordering letters by their mean‐position
    assign = {}        # assign[j] = letter
    used_big   = set()
    used_small = set()
    # sort letters by their average initial index
    order = sorted(positions.keys(), key=lambda ch: sum(positions[ch])/len(positions[ch]))
    for ch in order:
        need_big   = x[ch]
        need_small = t[ch] - x[ch]
        meanpos    = sum(positions[ch]) / len(positions[ch])

        # pick need_big nearest from big_classes not yet used
        candidates = [(abs(center - meanpos), j) for center,j in big_classes if j not in used_big]
        candidates.sort()
        for _, j in candidates[:need_big]:
            assign[j] = ch
            used_big.add(j)

        # same for small
        candidates = [(abs(center - meanpos), j) for center,j in small_classes if j not in used_small]
        candidates.sort()
        for _, j in candidates[:need_small]:
            assign[j] = ch
            used_small.add(j)

    # 5) now we know exactly which classes go to which letter; build the final positions
    #    and sum |init - final| in sorted‐matched order
    total_moves = 0
    for ch, init_list in positions.items():
        final_list = []
        for j in range(r):
            if assign.get(j) == ch:
                cnt = f[j]
                for k in range(cnt):
                    final_list.append(j + k*r)
        init_list.sort()
        final_list.sort()
        for a, b in zip(init_list, final_list):
            total_moves += abs(a - b)
    return total_moves

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    idx = 1
    out = []
    from collections import defaultdict
    for _ in range(t):
        n = int(data[idx]);  idx+=1
        S = data[idx];      idx+=1
        # gather initial positions
        pos = defaultdict(list)
        for i,ch in enumerate(S):
            pos[ch].append(i)
        counts = [len(pos[ch]) for ch in pos]
        # 1) minimal regularity
        r = min_regularity(counts, n)
        # 2) minimal moves for that r
        a = min_moves_for_r(pos, n, r)
        out.append(f"{r} {a}")
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()