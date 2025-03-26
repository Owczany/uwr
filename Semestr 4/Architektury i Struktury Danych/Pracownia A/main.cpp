// Piotr Pijanowski 346952
// Pracownia A - Układanie kafelkow


//! Pomysł 
/*
3 Zbiory ---> (kafelki_startowe, srodkowe_kafelki ('laczniki'), konocowe_kafelki)
Podczas wczytywania danych sprawdzamy czy startowe łączą się z końcowymi plus case: 0 m 0 sprawdzamy
zauwazylem ze laczniki l == r sa bezsensu bo one nie pomagaja w znalezieniu sciezki tylko wydluzaja kafelki
Nie ma sensu robić backtrackingu bo i tak jesli przejdziemy po jednym kafelku nie znajdziemy drogi to znaczy, ze tej sciezki nie ma za pomoca tego kafelka
*/

#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstdio>

using namespace std;

// Struktura kostki
struct Brick {
    unsigned short l, m, r;
    bool visited;
};

// Mapy przechowujące startowe, środkowe i końcowe kostki
unordered_map<unsigned short, Brick> starting_bricks;
unordered_map<unsigned short, Brick> ending_bricks;
unordered_map<unsigned short, unordered_map<unsigned short, Brick>> middle_bricks;

vector<Brick> wynik; // Przechowuje aktualnie budowany chodnik

bool find_path(unsigned short x) {
    auto it = middle_bricks.find(x);
    if (it == middle_bricks.end()) return false; // Jeśli nie ma połączeń to przerwij z negatywnym wynikiem

    for (auto &[key, b] : it->second) {
        if (b.visited) continue; // Pomijamy już odwiedzone klocki

        b.visited = true; // Jeśli kosta raz została odwiedzona to juz nigdy do niej nie wracamy
        wynik.push_back(b);

        // Jeśli jest połączenie z kafelkiem końcowym, to kończymy program
        if (ending_bricks.count(key)) {
            wynik.push_back(ending_bricks[key]);
            return true;
        }

        if (find_path(key)) return true; // Szukamy ściezki

        wynik.pop_back();
    }

    return false;
}

int main() {
    int n;
    scanf("%d", &n);

    wynik.reserve(n);

    unsigned short l, m, r;
    for (int i = 0; i < n; ++i) {
        scanf("%hu %hu %hu", &l, &m, &r);

        if (l == r && l != 0) continue; // Optymalizacja: pomijamy bezużyteczne klocki

        Brick brick = {l, m, r, false};

        // Kafelki początkowe
        if (l == 0) {
            // Kafelek {0, m, 0}
            if (r == 0) {
                printf("1\n%hu %hu %hu\n", l, m, r);
                return 0;
            }

            // Sprawdzamy bezpośrednie połączenia między startowym klockiem, a końcowym
            auto it = ending_bricks.find(r);
            if (it != ending_bricks.end())
            {
                printf("2\n%hu %hu %hu\n%hu %hu %hu\n", l, m, r, it->second.l, it->second.m, it->second.r);
                return 0;
            }

            starting_bricks[r] = brick;
        } 
        else if (r == 0) {
            // Sprawdzamy bezpośrednie połączenia między startowym klockiem, a końcowym
            auto it = starting_bricks.find(l);
            if (it != starting_bricks.end())
            {
                printf("2\n%hu %hu %hu\n%hu %hu %hu\n", it->second.l, it->second.m, it->second.r, l, m, r);
                return 0;
            }

            ending_bricks[l] = brick;
        } 
        else {
            middle_bricks[l][r] = brick;
        }
    }

    // Sprawdzanie szybkie, czy są kafelki startowe i początkowe
    if (starting_bricks.empty() || ending_bricks.empty()) {
        printf("BRAK\n");
        return 0;
    }

    // Rozwiązanie
    // Zaczynamy zawsze od kafelkw startowych i szukamy ściezki
    for (const auto &[key, starting_brick] : starting_bricks) {
        wynik.push_back(starting_brick);

        if (find_path(key)) {
            printf("%lu\n", wynik.size());
            for (const auto &b : wynik) {
                printf("%hu %hu %hu\n", b.l, b.m, b.r);
            }
            return 0;
        } 

        wynik.pop_back();
    }

    // Jeśli nie ma rozwiązania wypisz BRAK
    printf("BRAK\n");
    return 0;
}
