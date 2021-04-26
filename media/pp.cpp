#include<bits/stdc++.h>
using namespace std;

const int N = 21 * 10e4;
int S[N];
int D[N];

int query(int a, int b, int w, int lo, int hi) {
    if (a == lo && b == hi) return S[w];
    if (a >= b) return 0;
    int mid = (lo + hi) / 2;
    int L = query(a, min(mid, b), w*2, lo, mid);
    int R = query(max(a, mid), b, w*2+1, mid, hi);
    return L + R;
}

void update(int a, int b, int w, int lo, int hi, int val) {
    if (a == lo && b == hi) {
        if (D[w] != val) {
            D[w] = val;
            S[w] = (hi - lo) * D[w];
        }
        return;
    }
    if (a >= b) return;
    if (D[w] != -1) {
        D[w*2] = D[w];
        D[w*2+1] = D[w];
        D[w] = -1;
        S[w*2] = S[w]/2;
        S[w*2+1] = S[w]/2;
    }
    int mid = (lo + hi) / 2;
    update(a, min(mid, b), w*2, lo, mid, val);
    update(max(a, mid), b, w*2+1, mid, hi, val);
    S[w] = S[w*2] + S[w*2+1];
}

int find_power(int x) {
    int res = 1;
    while (x > res) {
        res *= 2;
    }
    return res;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, m, a, b;
    char c;

    cin >> n >> m;

    int size = find_power(n);

    for (int i = 1; i < size*2; i++) {
        if (i < size) D[i] = -1;
        else D[i] = 0;
    }

    for (int i = 0; i < m; i++) {
        cin >> a >> b >> c;
        if (c == 'C') {
            update(a-1, b, 1, 0, size, 0);
        }
        else {
            update(a-1, b, 1, 0, size, 1);
        }
        cout << query(0, size, 1, 0, size) << "\n";
    }   

    return 0;
}