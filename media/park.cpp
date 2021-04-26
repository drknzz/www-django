#include<bits/stdc++.h>
using namespace std;

#define X first
#define Y second

const int N = 500007;
const int H = 21;   //poss 19
int S = 0;
int Depth[N];
int Links[H][N];
int Left[N];
int Right[N];
int Parent[N];
pair<int, int> FarDown[N];
pair<int, int> FarUp[N];
pair<int, int> Far[N];

void clear() {
    for (int i = 0; i < N; i++) {
        Parent[i] = Left[i] = Right[i] = -1;
    }
}

int power(int x, int y) {
    while (--y) {
        x *= x;
    }
    return x;
}

void setDepth(int w, int d) {
    Depth[w] = d;
    if (Left[w] != -1) {
        setDepth(Left[w], d+1);
    }
    if (Right[w] != -1) {
        setDepth(Right[w], d+1);
    }
}

int ancestor(int w, int h) {
    if (!h) return w;
    if (h == 1) return Parent[w];
    if (h == Depth[w]) return 1;

    int result = w, power = S, jump = 2;

    for (int i = 0; i < power - 1; i++) {
        jump *= jump;
    }

    while (h) {
        if (jump > h) {
            jump /= 2;
            power--;
        }
        else {
            result = Links[power][result];
            h -= jump;
        }
    }

    return result;
}

int lca(int a, int b) {
    if (Depth[a] > Depth[b]) {
        a = ancestor(a, Depth[a] - Depth[b]);
    }
    else if (Depth[a] < Depth[b]) {
        b = ancestor(b, Depth[b] - Depth[a]);
    }

    if (a == b) return a;

    int power = S;

    while (power) {
        if (Links[power][a] != Links[power][b]) {
            a = Links[power][a];
            b = Links[power][b];
        }
        power--;
    }

    return Parent[a];
}

void setFarDown(int w) {
    if (Left[w] != -1) setFarDown(Left[w]);
    if (Right[w] != -1) setFarDown(Right[w]);

    FarDown[w] = make_pair(w, 0);
    if (Left[w] != -1 && FarDown[Left[w]].Y + 1 > FarDown[w].Y) {
        FarDown[w] = FarDown[Left[w]];
        FarDown[w].Y++;
    }
    if (Right[w] != -1 && FarDown[Right[w]].Y + 1 > FarDown[w].Y) {
        FarDown[w] = FarDown[Right[w]];
        FarDown[w].Y++;
    }
}

void setFarUp(int w) {
    FarUp[w] = make_pair(w, 0);
    if (Parent[w] != -1 && FarUp[Parent[w]].Y + 1 > FarUp[w].Y) {
        FarUp[w] = FarUp[Parent[w]];
        FarUp[w].Y++;
    }
    int sibling = -1;
    if (Parent[w] != -1) {
        if (Left[Parent[w]] == w) sibling = Right[Parent[w]];
        else sibling = Left[Parent[w]];
    }
    if (sibling != -1 && FarDown[sibling].Y + 2 > FarUp[w].Y) {
        FarUp[w] = FarDown[sibling];
        FarUp[w].Y += 2;
    }

    if (Left[w] != -1) setFarUp(Left[w]);
    if (Right[w] != -1) setFarUp(Right[w]);
}

void setFar(int n) {
    for (int i = 1; i <= n; i++) {
        if (FarDown[i].Y > FarUp[i].Y) Far[i] = FarDown[i];
        else Far[i] = FarUp[i];
    }
}

int query(int a, int d) {
    pair<int, int> p = Far[a];

    if (d > p.Y) return -1;

    int anc = lca(a, p.X);

    if (Depth[a] - Depth[anc] < d) {
        return ancestor(p.X, p.Y - d);
    }

    return ancestor(a, d);
}

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    clear();

    int n, m, a, d;
    pair<int, int> p;
    cin>>n;
    S = floor(log2(n));

    for (int i = 1; i <= n; i++) {
        cin>>Left[i]>>Right[i];
        if (Left[i]) Parent[Left[i]] = i;
        if (Right[i]) Parent[Right[i]] = i;
    }

    for (int i = 1; i <= n; i++) {
        Links[0][i] = Parent[i];
    }

    for (int i = 1; i <= S; i++) {       //poss
        for (int j = 1; j <= n; j++) {
            if (Links[i-1][j] != -1)
                Links[i][j] = Links[i-1][Links[i-1][j]];
            else Links[i-1][j] = -1;
        }
    }

    // for (int i = 0; i < H; i++) {
    //     for (int j = 0; j <= n + 2; j++) {
    //         cout<<Links[i][j]<<" ";
    //     }
    //     cout<<"\n";
    // }

    // return 0;

    setDepth(1, 0);
    setFarDown(1);
    setFarUp(1);
    setFar(n);

    // for (int i = 0; i < n+3; i++) {
    //     cout<<i<<": "<<FarDown[i].X<<" "<<FarDown[i].Y<<"\n";
    // }
    // cout<<endl<<endl;
    // for (int i = 0; i < n+3; i++) {
    //     cout<<i<<": "<<FarUp[i].X<<" "<<FarUp[i].Y<<"\n";
    // }
    // cout<<endl<<endl;
    // for (int i = 0; i < n+3; i++) {
    //     cout<<i<<": "<<Far[i].X<<" "<<Far[i].Y<<"\n";
    // }

    // for (int i = 0; i <= n + 1; i++) {
    //     cout<<i<<": "<<Depth[i]<<endl;
    // }
    cin>>m;

    for (int i = 0; i < m; i++) {
        cin>>a>>d;
        cout<<query(a, d)<<"\n";
    }

    return 0;
}