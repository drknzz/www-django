#include<bits/stdc++.h>
using namespace std;

#define X first
#define Y second

using pii = pair<int, int>;

const int INF = 10e8 + 7;
const int N = 200007;

pair<int, pii> V[N];
int D[N];
set<int> E[N];
priority_queue<pii, vector<pii>, greater<>> pq;
bool visited[N];

bool sortbysec(const pair<int, pii>& a, const pair<int, pii>& b) {
    return a.Y < b.Y;
}

bool sortbysecsec(const pair<int, pii>& a, const pair<int, pii>& b) {
    return a.Y.Y < b.Y.Y;
}

void update(int index) {
    // cout << index << endl;
    visited[index] = true;

    int new_length;
    for (int island : E[index]) {
        if (visited[island])
            continue;
        
        new_length = min(abs(V[index].Y.X - V[island].Y.X), abs(V[index].Y.Y - V[island].Y.Y));
        D[island] = min(D[island], D[index] + new_length);
        pq.push(make_pair(D[island], island));
    }
}

void dijkstra() {
    pii top;
    while (!pq.empty()) {
        top = pq.top();
        pq.pop();
        if (!visited[top.Y] && top.X <= D[top.Y])
            update(top.Y);
    }
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, x, y;

    cin >> n;

    for (int i = 0; i < n; i++) {
        cin >> x >> y;
        V[i] = make_pair(i, make_pair(x, y));
    }

    sort(V, V+n, sortbysec);

    for (int i = 0; i < n; i++) {
        if (i - 1 >= 0)
            E[V[i].X].insert(V[i-1].X);
        
        if (i + 1 < n)
            E[V[i].X].insert(V[i+1].X);
    }

    sort(V, V+n, sortbysecsec);

    for (int i = 0; i < n; i++) {
        if (i - 1 >= 0)
            E[V[i].X].insert(V[i-1].X);
        
        if (i + 1 < n)
            E[V[i].X].insert(V[i+1].X);
    }

    sort(V, V+n);

    // for (int i = 0; i < n; i++) {
    //     for (auto j = E[i].begin(); j != E[i].end(); j++) {
    //         cout << *j << ": " << V[*j].Y.X << " " << V[*j].Y.Y << " | ";
    //     }
    //     cout << "\n";
    // }

    D[0] = 0;
    pq.push(make_pair(D[0], 0));

    for (int i = 1; i < n; i++) {
        D[i] = INF;
    }

    dijkstra();

    // for (int i = 0; i < n; i++) {
    //     cout << i << ": " << D[i] << "\n";
    // }
    // cout <<"\n";
    cout << D[n-1] << "\n";

    return 0;
}

/*
5
2 2
1 1
4 5
7 1
6 7
*/