import random

# Parametry generowania danych
n = 200000  # Maksymalna liczba kostek
L_MAX = 10000
M_MAX = 10000
R_MAX = 10000

# Generowanie unikalnych kostek o "oddalonych" wartościach
kostki = set()

while len(kostki) < n:
    l = random.randint(0, L_MAX)
    m = random.randint(1, M_MAX)
    r = random.randint(0, R_MAX)

    # Tworzymy kostki, które nie są "ciągłe" dla zwiększenia losowości
    if l % 3 == 0 and r % 5 == 0:  
        kostki.add((l, m, r))

# Zamieniamy zestaw na listę i mieszamy, aby dodatkowo utrudnić znalezienie chodnika
kostki = list(kostki)
random.shuffle(kostki)

# Zapisywanie do pliku
file_path = "losowe_dane.txt"
with open(file_path, "w") as f:
    f.write(f"{len(kostki)}\n")  # Pierwsza linia: liczba kostek
    for l, m, r in kostki:
        f.write(f"{l} {m} {r}\n")

