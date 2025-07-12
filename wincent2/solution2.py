from __future__ import annotations
import sys
from collections import deque

"""helpers"""
def rotate_ccw(g: list[str]) -> list[str]:
    # 90 deg counter clockwise
    h, w = len(g), len(g[0])
    return [''.join(g[r][c] for r in range(h)) for c in range(w - 1, - 1, -1)]

def flip_h(g: list[str]) -> list[str]:
    # reverse each row
    return [row[::-1] for row in g]

def variants(g: list[str]) -> list[list[str]]:
    # return 8 transforms of g (rowtations x optional flip)
    outs = []
    for base in (g, flip_h(g)):
        cur = base
        for _ in range(4):
            outs.append(cur)
            cur = rotate_ccw(cur)
    return outs
    
"""row distort matcher"""
def inserted_row_ok(row: str, up: str, down: str) -> bool:
    # true if every col == either char in up or down
    return all((ch == up[i] or ch == down[i]) for i, ch in enumerate(row))

def match_with_row_insertions(img: list[str], ref: list[str]) -> bool:

    h, r = len(ref), len(img)
    if r < h or img[0] != ref[0] or img[-1] != ref[-1]:
        return False
    
    seen = [[False]*(r) for _ in range(h)]
    dq:deque[tuple[int, int]] = deque([(0, 0)])
    seen[0][0] = True

    while dq:
        i, j = dq.popleft()
        if i == h-1 and j == r-1:
            return True
        if j+1 >= r:
            continue
        
        nxt = img[j+1]
        if i+1 < h and nxt == ref[i+1] and not seen[i+1][j+1]:
            seen[i+1][j+1] = True
            dq.append((i+1, j+1))
        if i+1 < h and inserted_row_ok(nxt, ref[i], ref[i+1]) and not seen[i][j+1]:
            seen[i][j+1] = True
            dq.append((i, j+1))
    return False


"""read digit templates"""

def load_templates(path: str) -> list[list[list[str]]]:

    with open(path) as f:
        lines = [ln.rstrip() for ln in f]
    
    blocks, cur = [], []
    for ln in lines:
        if ln == '':
            if cur:
                blocks.append(cur)
                cur = []
        else:
            cur.append(ln)
    if cur:
        blocks.append(cur)
    if len(blocks) != 10:
        sys.exit("file must contain 10 digit bitmaps")

    return [variants(b) for b in blocks] # 10 x 8 grid


"""main"""
def identify_digits(template_file: str, input_file: str) -> None:
    templates = load_templates(template_file)

    with open(input_file) as f:
        t = int(f.readline())
        for _ in range(t):
            r, c = map(int, f.readline().split())
            img = [f.readline().strip() for _ in range(r)]

            ans = '?'
            for d in range(10):
                for g in templates[d]:
                    if len(g[0]) != c:
                        continue
                    if match_with_row_insertions(img, g):
                        ans = str(d)
                        break
                if ans != '?':
                    break
            print(ans)

"""cli"""
if __name__ == "__main__":
    if len(sys.argv) == 3:
        tpl, inp = sys.argv[1], sys.argv[2]
    elif len(sys.argv) == 2:
        tpl, inp = "D_digits.txt", sys.argv[1]
    else:
        sys.exit("incorrect usage")
    identify_digits(tpl, inp)