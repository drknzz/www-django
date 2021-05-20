#include<bits/stdc++.h>
using namespace std;

#define X first
#define Y second

typedef long long ll;

const int N = 200007;
pair<pair<int, int>, ll> tab[N];
ll res[N];

bool comp(const pair<pair<int, int>, int> &a, const pair<pair<int, int>, int> &b) {
    return a.X.Y < b.X.Y;
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, l, r;
    ll m = 0;
    cin >> n;
    for (int i = 0; i < n; ++i) {
        cin >> tab[i].X.X >> tab[i].X.Y >> tab[i].Y;
    }

    sort(tab, tab+n, comp);

    int j;

    res[0] = tab[0].Y;

    for (int i = 1; i < n; ++i) {

        l = 0;
        r = i - 1;

        while (l < r) {
            j = (l + r + 1) / 2;
            if (tab[j].X.Y < tab[i].X.X) {
                l = j;
            }
            else {
                r = j - 1;
            }
        }

        if (tab[r].X.Y < tab[i].X.X) {
            res[i] = max(res[i-1], tab[i].Y + res[r]);
        }
        else {
            res[i] = max(res[i-1], tab[i].Y);
        }

        m = max(m, res[i]);
    }

    cout << m << "\n";
}

/*

4
1 5 100
10 13 200
17 20 300
13 17 400

*/