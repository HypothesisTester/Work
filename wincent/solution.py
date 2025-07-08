#!/usr/bin/env python3
#  Two moves with rooks  – correct version
#
#  1 white move  ➜  1 black move   –  count all ordered pairs  (mod 1e9+7)
#
#  Public limits (t ≤ 30, d,n ≤ 100) are tiny, so the straightforward
#  “try every white move, then count every black move” strategy is fine
#  and completely deterministic.
#
#  --------------------------------------------------------------
#  Run:
#       python3 rooks_two_moves.py   <  input.txt   >  output.txt
#  --------------------------------------------------------------

import sys, bisect
MOD = 1_000_000_007


# ────────────────────────────────────────────────────────────────
# Utilities for the ordered lists that hold occupied squares
# ────────────────────────────────────────────────────────────────
def _ins(a, x): bisect.insort_left(a, x)
def _del(a, x): a.pop(bisect.bisect_left(a, x))


# ────────────────────────────────────────────────────────────────
# Number of legal moves for ONE black rook on the current board
# ────────────────────────────────────────────────────────────────
def black_moves(br, bc, d, pos2col, row_occ, col_occ):
    mv = 0

    # ----- horizontal -----
    row = row_occ[br]
    i = bisect.bisect_left(row, bc)

    left  = row[i-1]           if i           else None
    right = row[i+1]           if i+1 < len(row) else None

    # leftwards
    if left is None:
        mv += bc
    else:
        mv += bc - left - 1
        if pos2col[(br, left)] == 'W': mv += 1   # capture
    # rightwards
    if right is None:
        mv += d - bc - 1
    else:
        mv += right - bc - 1
        if pos2col[(br, right)] == 'W': mv += 1

    # ----- vertical -----
    col = col_occ[bc]
    i = bisect.bisect_left(col, br)

    up   = col[i-1]            if i           else None
    down = col[i+1]            if i+1 < len(col) else None

    # upward
    if up is None:
        mv += br
    else:
        mv += br - up - 1
        if pos2col[(up, bc)] == 'W': mv += 1
    # downward
    if down is None:
        mv += d - br - 1
    else:
        mv += down - br - 1
        if pos2col[(down, bc)] == 'W': mv += 1

    return mv


# ────────────────────────────────────────────────────────────────
# All legal destinations for one white rook (public d ≤ 100 → scan)
# ────────────────────────────────────────────────────────────────
def white_destinations(r, c, d, pos2col):
    res = []
    for dr, dc in ((0,-1),(0,1),(-1,0),(1,0)):
        rr, cc = r+dr, c+dc
        while 0 <= rr < d and 0 <= cc < d:
            if (rr, cc) in pos2col:
                if pos2col[(rr, cc)] == 'B':      # capture
                    res.append((rr, cc))
                break                             # own piece blocks
            res.append((rr, cc))                  # empty square
            rr += dr;  cc += dc
    return res


# ────────────────────────────────────────────────────────────────
# Main solver
# ────────────────────────────────────────────────────────────────
def solve():
    it   = iter(sys.stdin.buffer.read().split())
    t    = int(next(it))
    out  = []

    for _ in range(t):
        d, n = int(next(it)), int(next(it))

        pos2col = {}
        row_occ = [[] for _ in range(d)]
        col_occ = [[] for _ in range(d)]
        whites, blacks = [], []

        for _ in range(n):
            r, c, col = int(next(it)), int(next(it)), next(it).decode()
            pos2col[(r, c)] = col
            row_occ[r].append(c)
            col_occ[c].append(r)
            (whites if col == 'W' else blacks).append((r, c))

        for lst in row_occ: lst.sort()
        for lst in col_occ: lst.sort()

        black_set = set(blacks)
        ans = 0

        # ------------------------------------------------------
        # try every white move, then count the black moves left
        # ------------------------------------------------------
        for wr, wc in whites:
            for nr, nc in white_destinations(wr, wc, d, pos2col):

                # --- perform the white move ---
                _del(row_occ[wr], wc);  _del(col_occ[wc], wr)
                del pos2col[(wr, wc)]

                captured_black = (nr, nc) in pos2col
                if captured_black:
                    _del(row_occ[nr], nc);  _del(col_occ[nc], nr)
                    del pos2col[(nr, nc)]
                    black_set.remove((nr, nc))

                _ins(row_occ[nr], nc);  _ins(col_occ[nc], nr)
                pos2col[(nr, nc)] = 'W'

                # if at least one black rook survived, count its moves
                if black_set:
                    subtotal = 0
                    for br, bc in black_set:
                        subtotal += black_moves(br, bc, d, pos2col,
                                                row_occ, col_occ)
                    ans = (ans + subtotal) % MOD

                # --- rollback ---
                _del(row_occ[nr], nc);  _del(col_occ[nc], nr)
                del pos2col[(nr, nc)]

                if captured_black:
                    _ins(row_occ[nr], nc);  _ins(col_occ[nc], nr)
                    pos2col[(nr, nc)] = 'B'
                    black_set.add((nr, nc))

                _ins(row_occ[wr], wc);  _ins(col_occ[wc], wr)
                pos2col[(wr, wc)] = 'W'

        out.append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()