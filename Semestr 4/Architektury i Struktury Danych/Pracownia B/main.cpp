
#include <iostream>
#include <vector>
#include <cstdio>

using namespace std;


// void przesun_w_gore(array<int> K, int i) {
//     int k = i;

// }

void przesun_w_dol() {

}

int main()
{
    int M, k;
    int i;
    std::cin >> M >> k; // Wczytanie dwóch liczb

    // Obliczenie wymaganej wielkości tablicy
    int size = (M * (M + 1)) / 2;

    // Dynamiczna alokacja tablicy
    long long *arr = new long long[size];

    // Przykładowe przypisanie wartości
    i = 0;
    for (int row = 1; row <= M; ++row)
    {
        for (int col = row; col <= M; ++col)
        {
            arr[i++] = row * col; 
        }
    }

    // Przykładowe wyświetlenie wartości
    for (int i = 0; i < size; ++i)
    {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;

    // Zwolnienie pamięci
    delete[] arr;

    return 0;
}
