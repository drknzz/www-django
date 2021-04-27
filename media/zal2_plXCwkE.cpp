#include<bits/stdc++.h>
using namespace std;

#define X first
#define Y second

using pii = pair<int, int>;
using vpii = vector<pii>;
using vvpii = vector<vpii>;

const int INF = 10e8 + 7;
const pii neutral = make_pair(INF, 0);

int find_power(int x) {
    int res = 1;
    while (x > res) {
        res *= 2;
    }
    return res;
}

pii query_min_max(vpii& v, int a, int b, int w, int lo, int hi) {
    if (a <= lo && b >= hi) {
        return v[w];
    }
    if (a > hi || b < lo) {
        return neutral;
    }
    int mid = (lo + hi) / 2;
    pii L = query_min_max(v, a, b, w * 2, lo, mid);
    pii R = query_min_max(v, a, b, w * 2 + 1, mid + 1, hi);

    return make_pair(min(L.X, R.X), max(L.Y, R.Y));
}

pii query(vvpii& v, int x1, int x2, int w, int lo, int hi, int y1, int y2) {
    if (x1 <= lo && x2 >= hi) {
        return query_min_max(v[w], y1, y2, 1, 0, v[w].size() / 2 - 1);
    }
    if (x1 > hi || x2 < lo) {
        return neutral;
    }
    int mid = (lo + hi) / 2;
    pii L = query(v, x1, x2, w * 2, lo, mid, y1, y2);
    pii R = query(v, x1, x2, w * 2 + 1, mid + 1, hi, y1, y2);

    return make_pair(min(L.X, R.X), max(L.Y, R.Y));
}

void build_2d(vvpii& v) {
    for (size_t i = v.size()/2 - 1; i > 0; i--) {
        for (size_t j = 1; j < v[i].size(); j++) {
            v[i][j].X = min(v[i*2][j].X, v[i*2+1][j].X);
            v[i][j].Y = max(v[i*2][j].Y, v[i*2+1][j].Y);
        }
    }
}

void build(vvpii& v) {
    for (size_t i = v.size()/2; i < v.size(); i++) {
        for (size_t j = v[i].size()/2 - 1; j > 0; j--) {
            v[i][j].X = min(v[i][2*j].X, v[i][2*j+1].X);
            v[i][j].Y = max(v[i][2*j].Y, v[i][2*j+1].Y);
        }
    }
}


int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, m, k, x;

    cin >> n >> m >> k;
    int n_size = find_power(n);
    int m_size = find_power(m);

    vvpii v;
    vpii u(2 * m_size, make_pair(INF, 0));

    for (int i = 0; i < 2 * n_size; i++) {
        v.push_back(u);
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> x;
            v[i + n_size][j + m_size] = make_pair(x, x);
        }
    }

    build(v);
    build_2d(v);

    int x1, x2, y1, y2;

    for (int i = 0; i < k; i++) {
        cin >> x1 >> y1 >> x2 >> y2;
        pii res = query(v, x1, x2, 1, 0, n_size-1, y1, y2);
        cout << res.Y - res.X << endl;
    }

    return 0;
}

/*
3 6 5
2 3 2 1 5 8
4 3 5 2 7 1
1 6 3 5 8 3
0 0 2 2
0 2 1 4
1 5 2 5
1 2 2 4
1 1 1 1
*/