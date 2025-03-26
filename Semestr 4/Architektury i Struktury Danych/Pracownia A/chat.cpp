#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <cstdio>

using namespace std;

struct Brick {
    unsigned short l, m, r;
    bool visited;
};

// Mapy przechowujące startowe i końcowe kostki
unordered_map<unsigned short, Brick> starting_bricks;
unordered_map<unsigned short, Brick> ending_bricks;
unordered_map<unsigned short, unordered_map<unsigned short, Brick>> middle_bricks;

vector<Brick> wynik; // Przechowuje aktualnie budowany chodnik

bool find_path(unsigned short x) {
    auto it = middle_bricks.find(x);
    if (it == middle_bricks.end()) return false; // Brak połączeń

    for (auto &[key, b] : it->second) {
        if (b.visited) continue; // Pomijamy już odwiedzone klocki

        b.visited = true;
        wynik.push_back(b);

        if (ending_bricks.count(key)) {
            wynik.push_back(ending_bricks[key]);
            return true;
        }

        if (find_path(key)) return true;

        b.visited = false;
        wynik.pop_back();
    }

    return false;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);

    int n;
    scanf("%d", &n); // Szybsze wczytywanie

    // wynik.reserve(n); // Rezerwujemy pamięć dla wektora wynik

    unsigned short l, m, r;
    for (int i = 0; i < n; ++i) {
        scanf("%hu %hu %hu", &l, &m, &r);

        if (l == r) continue; // Optymalizacja: pomijamy bezużyteczne klocki

        Brick brick = {l, m, r, false};

        if (l == 0) {
            if (r == 0) {
                printf("1\n%hu %hu %hu\n", l, m, r);
                return 0;
            }

            if (!starting_bricks.count(r)) starting_bricks[r] = brick;
        } 
        else if (r == 0) {
            if (!ending_bricks.count(l)) ending_bricks[l] = brick;
        } 
        else {
            if (!middle_bricks[l].count(r)) middle_bricks[l][r] = brick;
        }
    }

    if (starting_bricks.empty() || ending_bricks.empty()) {
        printf("BRAK\n");
        return 0;
    }

    for (const auto &[key, b] : starting_bricks) {
        wynik.push_back(b);

        if (find_path(key)) {
            printf("%lu\n", wynik.size());
            for (const auto &b : wynik) {
                printf("%hu %hu %hu\n", b.l, b.m, b.r);
            }
            return 0;
        } 

        wynik.pop_back();
    }

    printf("BRAK\n");
    return 0;
}
