// Piotr Pijanowski 346952
// Pracownia A - Kostki
// 


//! 

#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <chrono>

using namespace std;

// Struktura naszej kostki, przechowująca trzy wartości
struct Brick
{
    unsigned short l, m, r;
    bool visited;
};

// Mapy przechowujące startowe i końcowe kostki
unordered_map<unsigned short, Brick> starting_bricks;
unordered_map<unsigned short, Brick> ending_bricks;
unordered_map<unsigned short, unordered_map<unsigned short, Brick> > middle_bricks;

vector<Brick> wynik; // Przechowuje aktualnie budowany chodnik


bool find_path(unsigned short x) {
    for (auto &[key, b] : middle_bricks[x]) {
        if (b.visited) {
            return false;
        }

        b.visited = true;

        wynik.push_back(b);
        // Jeśli r jest już w ending_bricks, wypisz oba bloki
        // Dodać koniec programu, zeby jeśli znalazł to juz nie ma rekurancji
        if (ending_bricks.count(key))
        {
            wynik.push_back(ending_bricks[key]);
            return true;
        }

        // Napisać, ze usuwawa  przeszukiwana kostke 
        // if (starting_bricks.count(key))
        // {
        //     middle_bricks[x].erase(key);
        //     wynik.pop_back();
        //     return false;
        // }
        // Dalsze szukanie środkowego kafelka
        if (find_path(key)) {
            // wynik.pop_back();
            return true;
        }
        wynik.pop_back();
    }
    return false;
}

// Glowna funkcja
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    unsigned short l, m, r;
    int n;
    cin >> n;

    for (int i = 0; i < n; ++i)
    {
        cin >> l >> m >> r;

        // wynik.reserve(n);
        Brick brick = {l, m, r, false}; // Tworzenie obiektu Brick

        if (l == 0)
        {
            // Corner case: l == 0 and r == 0, czyli kostki typu 0 m 0
            if (r == 0)
            {
                cout << 1 << '\n';
                cout << l << ' ' << m << ' ' << r;
                return 0;
            }

            // Jeśli r jest już w ending_bricks, wypisz oba bloki
            auto it = ending_bricks.find(r);
            if (it != ending_bricks.end())
            {
                cout << 2 << '\n';
                cout << l << ' ' << m << ' ' << r << '\n';
                cout << it->second.l << ' ' << it->second.m << ' ' << it->second.r << '\n';
                return 0;
            }

            // Dodanie kostki startowej, klucz to r
            starting_bricks[r] = brick;
        }
        else if (r == 0)
        {
            // Jeśli l jest już w starting_bricks, wypisz oba bloki
            auto it = starting_bricks.find(l);
            if (it != starting_bricks.end())
            {
                cout << 2 << '\n';
                cout << it->second.l << ' ' << it->second.m << ' ' << it->second.r << '\n';
                cout << l << ' ' << m << ' ' << r << '\n';
                return 0;
            }

            // Dodanie kostki końcowej, klucz to l
            ending_bricks[l] = brick;
        }
        else if (l == r)
        {
            continue;
        }
        else
        {
            middle_bricks[l][r] = brick;
        }
    }

    // Szybkie sprawdzenie, czy sytuacja w ogole ma rowiązanie
    if (starting_bricks.size() == 0 || ending_bricks.size() == 0)
    {
        cout << "BRAK" << '\n';
        return 0;
    }

    // Rozwiązanie zaczynamy sprawdzanie od kostek początkowych
    for (const auto &[key, b] : starting_bricks) {
        wynik.push_back(b);
        
        if (find_path(key)) {
             // Wypisz rozmiar vectora wynik
            cout << wynik.size() << '\n';

            // Wypisz jego elementy
            for (const auto &b : wynik) {
                cout << b.l << ' ' << b.m << ' ' << b.r << '\n';
            }
            return 0;
        } 

        wynik.pop_back();
    }

    cout << "BRAK" << '\n';
    return 0;
}
