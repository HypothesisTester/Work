

#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <utility>
#include <cstdint>
#include <cmath>

using int64 = long long;
const int64 MOD = 1'000'000'007LL;
const int64 INF = (1LL << 60);

/* ---------- tiny helpers for sorted “lines” (rows / columns) ---------- */
template <class Vec>
inline int idx_of(const Vec& v, int64 key) {
    return std::lower_bound(v.begin(), v.end(), key,
                            [](auto a, auto b) { return a.first < b; }) -
           v.begin();
}
template <class Vec>
inline auto left_piece(const Vec& v, int pos) -> std::pair<int64, char> {
    return pos ? v[pos - 1] : std::make_pair(-1LL, '?');
}
template <class Vec>
inline auto right_piece(const Vec& v, int pos) -> std::pair<int64, char> {
    return (pos + 1 < (int)v.size()) ? v[pos + 1]
                                     : std::make_pair(INF, '?');
}

/* ---------- mobility of ONE black rook once neighbours are known ------ */
inline int64 moves_black(int64 r, int64 c,
                         const std::vector<std::pair<int64, char>>& row,
                         const std::vector<std::pair<int64, char>>& col,
                         int ir, int ic, int64 D) {
    auto [cl, clCol] = left_piece(row, ir);
    auto [cr, crCol] = right_piece(row, ir);
    auto [ru, ruCol] = left_piece(col, ic);
    auto [rd, rdCol] = right_piece(col, ic);

    int64 leftE  = c - cl - 1;
    int64 rightE = (cr == INF ? D : cr) - c - 1;
    int64 upE    = r - ru - 1;
    int64 dnE    = (rd == INF ? D : rd) - r - 1;

    int64 capL = (cl != -1 && clCol == 'W');
    int64 capR = (cr != INF && crCol == 'W');
    int64 capU = (ru != -1 && ruCol == 'W');
    int64 capD = (rd != INF && rdCol == 'W');

    return (leftE + rightE + upE + dnE + capL + capR + capU + capD) % MOD;
}

/* ===================================================================== */
int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int T;
    if (!(std::cin >> T)) return 0;

    while (T--) {
        /* ---------- read input ---------- */
        int64 D; int n;
        std::cin >> D >> n;

        struct Piece { int64 r, c; char col; };
        std::vector<Piece> white, black;
        white.reserve(n); black.reserve(n);

        /* rows[r]  : sorted (col, colour)  on that row
           cols[c]  : sorted (row, colour)  on that column                */
        std::unordered_map<int64, std::vector<std::pair<int64,char>>> rows, cols;

        for (int i = 0; i < n; ++i) {
            int64 r, c; char t;  std::cin >> r >> c >> t;
            (t=='W'?white:black).push_back({r,c,t});
            rows[r].push_back({c,t});
            cols[c].push_back({r,t});
        }
        for (auto& kv : rows) std::sort(kv.second.begin(), kv.second.end());
        for (auto& kv : cols) std::sort(kv.second.begin(), kv.second.end());

        /* ---------- baseline: total mobility of every black rook ------- */
        int64 base = 0;
        for (auto& b : black) {
            auto &row = rows[b.r], &col = cols[b.c];
            int ir = idx_of(row, b.c);
            int ic = idx_of(col, b.r);
            base = (base + moves_black(b.r,b.c,row,col,ir,ic,D)) % MOD;
        }

        /* Prepare sorted lists of occupied rows / columns                 */
        std::vector<int64> occRows, occCols;
        occRows.reserve(rows.size()); occCols.reserve(cols.size());
        for (auto& kv: rows) occRows.push_back(kv.first);
        for (auto& kv: cols) occCols.push_back(kv.first);
        std::sort(occRows.begin(), occRows.end());
        std::sort(occCols.begin(), occCols.end());

        int64 sumWhiteMoves = 0;   // Σ |legal white destinations|
        int64 deltaSum      = 0;   // Σ (blackMobAfter − base)

        /* ---------- iterate every white rook --------------------------- */
        for (auto& w : white) {
            auto &rowW = rows[w.r], &colW = cols[w.c];
            int irW = idx_of(rowW, w.c);
            int icW = idx_of(colW, w.r);

            /* ---- neighbours of the white rook ---- */
            auto [cL , colL ] = left_piece (rowW, irW);
            auto [cR , colR ] = right_piece(rowW, irW);
            auto [rU , colU ] = left_piece (colW, icW);
            auto [rD , colD ] = right_piece(colW, icW);

            /* ---- constants: effect of VACATING (w.r, w.c) ------------- */
            int64 deltaVacate = 0;
            auto vacBonus = [&](int64 neighRow, int64 neighCol, int step) {
                /* step is +1 (below/right) or -1 (above/left) */
                if (neighRow==-1 || neighRow==INF) return;
                auto &rw = rows[neighRow], &cw = cols[neighCol];
                int ir = idx_of(rw , neighCol);
                int ic = idx_of(cw , neighRow);
                if (rw[ir].second != 'B') return;           // only black rooks
                int64 before = moves_black(neighRow,neighCol,rw,cw,ir,ic,D);
                /* after vacating, empty distance grows by 1
                   and capture possibility may appear            */
                int64 after  = (before + 1) % MOD;
                deltaVacate  = (deltaVacate + after - before + MOD) % MOD;
            };
            vacBonus(rU , w.c, -1);
            vacBonus(rD , w.c, +1);
            vacBonus(w.r, cL, -1);
            vacBonus(w.r, cR, +1);

            /* -----------------------------------------------------------
               Handle the four stretches the rook can slide on.
               For each stretch we use closed-form formulas:

               1) length ℓ  →  contributes ℓ empty-square moves
               2) sum_{k=1..ℓ} k  = ℓ(ℓ+1)/2
                  tells us how many times the “−1 per step” effect for a
                  neighbouring black rook accumulates while we slide.
            ----------------------------------------------------------- */

            auto process = [&](bool horizontal,
                               int64 fixed,        // row (if horizontal) or column
                               int64 start, int64 stop,  // neighbour, exclusive
                               int dir,            // −1 or +1
                               bool blkNear, bool blkFar)
            {
                int64 len = std::abs(stop - start) - 1;
                if (len == 0) return;

                /*  white-move count */
                sumWhiteMoves = (sumWhiteMoves + len) % MOD;

                /*  effect on black rook in the *near* direction:
                      Its free distance shrinks by 1, 2, …, len
                      →  total − Σ k  =  −len(len+1)/2
                 */
                int64 tri = (len * (len + 1) / 2) % MOD;
                if (blkNear) deltaSum = (deltaSum + MOD - tri) % MOD;
                if (blkFar)  deltaSum = (deltaSum + tri) % MOD; // far rook gains

                /*  vacating the origin benefits its column neighbours   */
                deltaSum = (deltaSum + deltaVacate * (len % MOD)) % MOD;
            };

            /* LEFT  stretch */
            process(true, w.r, cL, w.c, -1,
                    (cL!=-1 && colL=='B'),
                    (cR!=INF&& colR=='B'));
            /* RIGHT */
            process(true, w.r, w.c, cR, +1,
                    (cR!=INF&& colR=='B'),
                    (cL!=-1 && colL=='B'));
            /* UP    */
            process(false,w.c, rU, w.r, -1,
                    (rU!=-1 && colU=='B'),
                    (rD!=INF&& colD=='B'));
            /* DOWN  */
            process(false,w.c, w.r, rD, +1,
                    (rD!=INF&& colD=='B'),
                    (rU!=-1 && colU=='B'));

            /* ---------- the (≤4) capturing destinations --------------- */
            auto tryCapture = [&](int64 nr, int64 nc)
            {
                if(nr<0 || nr>=D || nc<0 || nc>=D) return;
                auto &row = rows[nr], &col = cols[nc];
                int ir = idx_of(row, nc);
                int ic = idx_of(col, nr);
                if (ir==(int)row.size() || row[ir].first!=nc ||
                    row[ir].second!='B') return;          // must be black

                /* moves lost by captured rook */
                int64 lost = moves_black(nr,nc,row,col,ir,ic,D);

                /* moves gained/lost by the ≤ 4 neighbouring black rooks */
                int64 around = 0;
                auto upd = [&](int64 r,int64 c){
                    if(r<0||r>=D||c<0||c>=D) return;
                    auto &rw=rows[r], &cw=cols[c];
                    int ir2=idx_of(rw,c), ic2=idx_of(cw,r);
                    if(ir2<(int)rw.size() && rw[ir2].first==c &&
                       rw[ir2].second=='B')
                        around = (around + moves_black(r,c,rw,cw,ir2,ic2,D))%MOD;
                };
                upd(nr-1,nc); upd(nr+1,nc); upd(nr,nc-1); upd(nr,nc+1);

                /* white rook lands on (nr,nc) – restrict those same
                   neighbours: they lose exactly one square of distance */
                int64 neighbours = 0;
                if(nr>0)         neighbours++;
                if(nr+1<D)       neighbours++;
                if(nc>0)         neighbours++;
                if(nc+1<D)       neighbours++;

                int64 delta = (MOD - lost + neighbours)%MOD;
                deltaSum = (deltaSum + delta) % MOD;
                sumWhiteMoves = (sumWhiteMoves + 1) % MOD;
            };
            tryCapture(w.r, cL);
            tryCapture(w.r, cR);
            tryCapture(rU, w.c);
            tryCapture(rD, w.c);
        }

        /* ---------------- final answer for this test case ------------- */
        int64 ans = ( (base % MOD) * (sumWhiteMoves % MOD) + deltaSum ) % MOD;
        std::cout << (ans + MOD) % MOD << '\n';
    }
    return 0;
}