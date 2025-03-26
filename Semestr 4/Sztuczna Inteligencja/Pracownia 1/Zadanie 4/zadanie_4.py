from collections import deque

# Plik wejściowy i wyjściowy
INPUT_FILE = 'zad4_input.txt'
OUTPUT_FILE = 'zad4_output.txt'

# Funkcja służąca do zczytania danych
def read_input_file(filename):
    """Odczytuje dane wejściowe z pliku."""
    with open(filename, 'r') as f:
        return [line.split() for line in f.readlines()]

# Funkcja służąca do zapisania wyniku
def write_output_file(filename, output):
    """Zapisuje wynik do pliku."""
    with open(filename, 'a') as f:
        f.write(f'{output}\n')


def count_blocks(arr):
    """Zlicza liczbę bloków jedynek w tablicy."""
    prev = arr[0]
    count = 1 if prev == 1 else 0
    for i in range(1, len(arr)):
        if not prev and arr[i]:
            count += 1
        prev = arr[i]
    return count


def opt_dist(arr, D):
    """BFS szukający minimalnej liczby zmian do uzyskania jednego bloku 1 o długości D."""
    if D == 0:
        return arr.count(1)  # Liczba jedynek do usunięcia

    visited = set()
    queue = deque([(arr, 0)])

    while queue:
        nono, moves = queue.popleft()

        # Sprawdzenie warunku końcowego
        if count_blocks(nono) == 1 and nono.count(1) == D:
            return moves

        # Oznaczamy stan jako odwiedzony
        state_tuple = tuple(nono)
        if state_tuple not in visited:
            visited.add(state_tuple)

            # Generowanie sąsiednich stanów
            for i in range(len(nono)):
                new_nono = nono.copy()
                new_nono[i] ^= 1  # Zamiana 0->1 lub 1->0
                if tuple(new_nono) not in visited:
                    queue.append((new_nono, moves + 1))


# Czyszczenie pliku wynikowego przed rozpoczęciem
open(OUTPUT_FILE, 'w').close()

# Odczyt i przetwarzanie wejścia
for line in read_input_file(INPUT_FILE):
    a, D = line
    result = opt_dist([int(t) for t in a], int(D))
    write_output_file(OUTPUT_FILE, str(result))
