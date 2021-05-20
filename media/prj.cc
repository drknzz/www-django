#include<bits/stdc++.h>
using namespace std;

const int N = 100007;

priority_queue<pair<int, int>, vector<pair<int, int>>, greater<>> pq;
vector<int> l[N];
int dep[N];
int prog[N];

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int n, m, k, a, b, sum = 0;
    int value, result = 0;
    cin >> n >> m >> k;

    for (int i = 1; i < n + 1; i++) {
        cin >> prog[i];
    }
    for (int i = 1; i < m + 1; i++) {
        cin >> a >> b;
        dep[a]++;
        l[b].push_back(a);
    }

    for (int i = 1; i < n + 1; i++) {
        if (!dep[i]) {
            pq.push(make_pair(prog[i], i));
        }
    }

    for (int i = 0; i < k; i++) {
        pair<int, int> top = pq.top();
        pq.pop();

        sum = max(sum, top.first);

        for (int x : l[top.second]) {
            dep[x]--;
            if (!dep[x]) pq.push(make_pair(prog[x], x));
        }
    }

    cout<<sum<<endl;

    return 0;
}

/*

5 3 3
10
500
150
200
100
1 2
1 3
4 5

*/