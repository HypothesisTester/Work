#!/usr/bin/env python3


import sys, math, random, itertools, collections
random.seed(1)

# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def is_feasible(order, objs, w0):
    """True iff the weight rule holds along *order*."""
    w = w0
    for i in order:
        z = objs[i][2]
        if w <= 2 * z:
            return False
        w += z
    return True


def compute_distance_matrix(objs):
    """dist[i][j], with -1 standing for the origin (0,0)."""
    n = len(objs)
    dist = [[0.0]*(n+1) for _ in range(n+1)]
    for i in range(n):
        xi, yi, _ = objs[i]
        d0 = math.hypot(xi, yi)
        dist[-1][i] = dist[i][-1] = d0
        for j in range(i+1, n):
            xj, yj, _ = objs[j]
            d = math.hypot(xi - xj, yi - yj)
            dist[i][j] = dist[j][i] = d
    return dist


def tour_length(order, dist):
    if not order:
        return 0.0
    d = dist[-1][order[0]]
    for a, b in zip(order, order[1:]):
        d += dist[a][b]
    return d


# ----------------------------------------------------------------------
# reachable set (weight scan)
# ----------------------------------------------------------------------
def reachable_indices(objs, w0):
    idx = sorted(range(len(objs)), key=lambda i: objs[i][2])
    w = w0
    reach = []
    for i in idx:
        zi = objs[i][2]
        if w > 2*zi:
            reach.append(i)
            w += zi
    return reach


# ----------------------------------------------------------------------
# feasibility repair (bubble light ones forward until rule holds)
# ----------------------------------------------------------------------
def repair(order, objs, w0):
    order = list(order)
    w = w0
    i = 0
    while i < len(order):
        if w > 2 * objs[order[i]][2]:
            w += objs[order[i]][2]
            i += 1
            continue
        # need a lighter object ahead – scan forward
        j = i+1
        while j < len(order) and w <= 2 * objs[order[j]][2]:
            j += 1
        if j == len(order):
            return None          # unreachable (should not happen)
        # bring order[j] to position i (stable)
        gene = order.pop(j)
        order.insert(i, gene)
    return order


# ----------------------------------------------------------------------
# seed generators
# ----------------------------------------------------------------------
def nearest_eligible_seed(R, objs, w0, dist):
    remaining = set(R)
    w = w0
    cur = -1     # origin
    tour = []
    while remaining:
        elig = [i for i in remaining if w > 2*objs[i][2]]
        nxt = min(elig, key=lambda i: dist[cur][i])
        tour.append(nxt)
        remaining.remove(nxt)
        w += objs[nxt][2]
        cur = nxt
    return tour


def weight_sorted_seed(R):
    return sorted(R, key=lambda i: objs[i][2])


def mst_preorder_seed(R, objs):
    # Prim on full graph is O(n²) anyway – trivial for n ≤ 200
    n = len(R)
    used = [False]*n
    parent = [-1]*n
    key = [float('inf')]*n
    key[0] = 0
    pts = [objs[i][:2] for i in R]
    for _ in range(n):
        u = min((k, i) for i, k in enumerate(key) if not used[i])[1]
        used[u] = True
        ux, uy = pts[u]
        for v in range(n):
            if not used[v]:
                vx, vy = pts[v]
                w = (ux-vx)**2 + (uy-vy)**2
                if w < key[v]:
                    key[v] = w
                    parent[v] = u
    # Build adjacency, DFS preorder
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        adj[parent[v]].append(v)
        adj[v].append(parent[v])
    order = []
    st = [0]
    seen = [False]*n
    while st:
        u = st.pop()
        if seen[u]:
            continue
        seen[u] = True
        order.append(R[u])
        for v in adj[u]:
            if not seen[v]:
                st.append(v)
    return order


def hilbert_seed(R, objs):
    def hilbert(x, y, bits=21):  # covers |coord| ≤ 1e7 < 2^24
        mask = 1 << (bits-1)
        h = 0
        xi = x + (1<<23)
        yi = y + (1<<23)
        for k in range(bits):
            rx = 1 if xi & (mask>>k) else 0
            ry = 1 if yi & (mask>>k) else 0
            h <<= 2
            h |= rx * 3 ^ ry
        return h
    return sorted(R, key=lambda i: hilbert(objs[i][0], objs[i][1]))


def zorder_seed(R, objs):
    def interleave(x, y, bits=21):
        x = x + (1<<23)
        y = y + (1<<23)
        inter = 0
        for i in range(bits):
            inter |= ((y >> i) & 1) << (2*i+1)
            inter |= ((x >> i) & 1) << (2*i)
        return inter
    return sorted(R, key=lambda i: interleave(objs[i][0], objs[i][1]))


# ----------------------------------------------------------------------
# local search moves (always keep **legal** tour)
# ----------------------------------------------------------------------
def two_opt(order, objs, w0, dist):
    n = len(order)
    improved = True
    while improved:
        improved = False
        for i in range(n-3):
            a, b = order[i], order[i+1]
            dab = dist[a][b]
            for j in range(i+2, n-1):
                c, d = order[j], order[j+1]
                if a == d or b == c:
                    continue
                before = dab + dist[c][d]
                after  = dist[a][c] + dist[b][d]
                if after + 1e-9 >= before:
                    continue
                cand = order[:i+1] + order[i+1:j+1][::-1] + order[j+1:]
                if is_feasible(cand, objs, w0):
                    order = cand
                    n = len(order)
                    improved = True
                    break
            if improved:
                break
    return order


def or_opt(order, objs, w0, dist):
    n = len(order)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            node = order[i]
            prev = -1 if i==0 else order[i-1]
            nxt  = -1 if i==n-1 else order[i+1]
            base_loss = 0.0
            if prev == -1:
                base_loss += dist[-1][node]
            else:
                base_loss += dist[prev][node]
            if nxt != -1:
                base_loss += dist[node][nxt]
            if prev != -1 and nxt != -1:
                base_gain_root = dist[prev][nxt]
            elif prev == -1 and nxt != -1:
                base_gain_root = dist[-1][nxt]
            else:
                base_gain_root = 0.0

            for j in range(n+1):
                if j==i or j==i+1:
                    continue
                prev_j = -1 if j==0 else order[j-1 if j<i else j-1]
                nxt_j  = -1 if j==n else order[j if j<i else j]
                loss = base_loss
                gain = base_gain_root
                if prev_j == -1:
                    gain += dist[-1][node]
                else:
                    gain += dist[prev_j][node]
                if nxt_j != -1:
                    gain += dist[node][nxt_j]
                    loss += dist[prev_j][nxt_j] if prev_j!=-1 else dist[-1][nxt_j]
                delta = gain - loss
                if delta + 1e-9 >= 0:
                    continue
                cand = order[:i]+order[i+1:]
                cand = cand[:j]+[node]+cand[j:]
                if is_feasible(cand, objs, w0):
                    order = cand
                    n = len(order)
                    improved = True
                    break
            if improved:
                break
    return order


def three_opt_once(order, objs, w0, dist):
    n = len(order)
    for (i,j,k) in itertools.combinations(range(1,n-1),3):
        a,b = order[i-1], order[i]
        c,d = order[j-1], order[j]
        e,f = order[k-1], order[k]
        choices = [
            order[:i] + order[i:j][::-1] + order[j:k][::-1] + order[k:],   # invert both
            order[:i] + order[j:k] + order[i:j] + order[k:],               # exchange segments
            order[:i] + order[j:k] + order[i:j][::-1] + order[k:]
        ]
        for cand in choices:
            if is_feasible(cand, objs, w0) and \
               tour_length(cand, dist) + 1e-9 < tour_length(order, dist):
                return cand
    return order


# ----------------------------------------------------------------------
# solve one test case
# ----------------------------------------------------------------------
def solve_case(objs, w0):
    R = reachable_indices(objs, w0)
    if not R:                    # nothing assimilatable
        return []

    dist = compute_distance_matrix(objs)
    best = None
    best_len = float('inf')

    # ---------- seeds ----------
    seeds = []
    seeds.append(nearest_eligible_seed(R, objs, w0, dist))
    seeds.append(weight_sorted_seed(R))
    seeds.append(mst_preorder_seed(R, objs))
    seeds.append(hilbert_seed(R, objs))
    seeds.append(zorder_seed(R, objs))

    # random shuffles  (+ feasibility repair)
    for _ in range(245):
        s = R[:]
        random.shuffle(s)
        s = repair(s, objs, w0)
        if s:
            seeds.append(s)

    # ---------- local search ----------
    for tour in seeds:
        if not is_feasible(tour, objs, w0):
            continue
        tour = two_opt(tour, objs, w0, dist)
        tour = or_opt(tour, objs, w0, dist)
        tour = three_opt_once(tour, objs, w0, dist)

        L = tour_length(tour, dist)
        if L < best_len - 1e-9:
            best = tour
            best_len = L

    return best


# ----------------------------------------------------------------------
def main():
    data = sys.stdin.read().split()
    if not data:
        return
    t = int(data[0]); idx = 1
    out = []
    global objs
    for _ in range(t):
        n  = int(data[idx]); idx += 1
        w0 = int(data[idx]); idx += 1
        objs = []
        for _ in range(n):
            x = int(data[idx]); y = int(data[idx+1]); z = int(data[idx+2])
            objs.append((x, y, z))
            idx += 3

        best_order = solve_case(objs, w0)
        out.append(str(len(best_order)))
        out.append(" ".join(map(str, best_order)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()