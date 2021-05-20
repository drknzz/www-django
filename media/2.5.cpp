#include<bits/stdc++.h>
using namespace std;

int tab[100];

int main() {
    
    //wczytanie danych
    int n, k;
    cin >> n >> k;
    for (int i = 0; i < n; i++) {
        cin >> tab[i];
    }
    
    k %= n;                 //modulo, aby k < n
    int nwd = __gcd(n, k);  //nwd z dł tablicy i dł przesunięcia
    int tmp, tmp2;
    int index = 0;
    
    for (int i = 0; i < nwd; i++) {         //nwd = ilość cykli jakie zrobimy
        index = i;                          //ustawiamy indeks na punkt startowy
        tmp = tab[index];                   //zapamietujemy wartosc pod startowym indeksem
        for (int j = 0; j < n / nwd; j++) { // (n/nwd) = dlugosc jednego cyklu
            index += (n-k);                 // k pozycji w lewo = n-k pozycji w prawo
            index %= n;                     //jezeli wyjdziemy poza zakres tablicy
            tmp2 = tab[index];              //zapamietujemy tab[index]
            tab[index] = tmp;               //przypisujemy wartosc z poprzedniej pozycji
            tmp = tmp2;                     //aktualizujemy indeks
        }
    }
    
    //wypisanie tablicy
    for (int i = 0; i < n; i++) {
        cout<<tab[i]<<" ";
    }
    cout<<endl;
    
    return 0;
}
