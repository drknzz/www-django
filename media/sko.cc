#include<bits/stdc++.h>
using namespace std;

#define X first
#define Y second

typedef long long ll;
typedef unsigned long long ull;
typedef pair<int, int> pii;
typedef vector<pii> vpii;
typedef vector<vpii> vvpii;

const int INF = 10e8;
const int N = 300007;

vpii v[N];
bitset<N> visited;
int dp[N][2];

enum type {
    TAKEN, FREE
};

void compute_dp(int node) {
    int children = 0;
    int path = 0;
    
    visited[node] = true;

    for (auto& x : v[node]) {
        if (!visited[x.X]) {
            compute_dp(x.X);

            children += max(dp[x.X][TAKEN], dp[x.X][FREE]);
            path = max(path, x.Y + dp[x.X][FREE] - max(dp[x.X][FREE], dp[x.X][TAKEN]));
        }
    }

    dp[node][FREE] = children;
    dp[node][TAKEN] = children + path;
}



int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, m, a, b, c;
    cin >> n;

    for (int i = 0; i < n - 1; ++i) {
        cin >> a >> b >> c;
        v[a].emplace_back(b, c);
        v[b].emplace_back(a, c);
    }

    compute_dp(1);

    cout << max(dp[1][FREE], dp[1][TAKEN]) << "\n";
}

/*

7
1 3 2
3 2 1
2 4 5
2 5 7
3 6 10
6 7 1

*/