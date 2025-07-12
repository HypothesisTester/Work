from __future__ import annotations
import sys
import os

def build_depth(max_n: int) -> list[int]:
    # distance of node i from the root (root depth = 0)
    depth = [0] * (max_n + 2) # +2 to access depth[2*i+1]
    for i in range(2, max_n + 1):
        depth[i] = depth[i >> 1] + 1 # parent is i//2, depth[parent] is know
    return depth

def heap_score(n: int, depth: list[int]) -> int:

    subtree = [0]*(n + 2) # subtree sizes (1-indexed, +1 sentinel)
    ans = 0

    # bottom up traversal
    for i in range(n, 0, -1):
        size = 1 # node itself
        child = i << 1 # left child index

        if child <= n: # add left subtree
            size += subtree[child]
            if child + 1 <= n: # add right subtree (if exists)
                size += subtree[child + 1]
        
        subtree[i] = size

        # admissable values for node form a contiguous interval
        lo = size
        hi = n - depth[i]

        if lo <= hi: # interval is non-empty
            ans += (hi*(hi + 1) - (lo - 1)*lo) // 2

    return ans

def main() -> None:
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        data_in = open(sys.argv[1]).read()
    else:
        data_in = sys.stdin.read()
    data = list(map(int, data_in.strip().split()))
    if not data:
        return
    t, *cases = data
    max_n = max(cases)

    depth = build_depth(max_n)

    out_lines = []

    for n in cases:
        out_lines.append(str(heap_score(n, depth)))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()