import math

# Funkcja f(x) i jej pochodna f'(x) dla przykładu f(x) = (x - alpha)^r
def f(x, alpha=2, r=2):
    return (x - alpha) ** r + 12*x + 18*x*x

def f_pochodna(x, alpha=2, r=2):
    return r * (x - alpha) ** (r - 1) + 12 + 18*x

# Funkcja iteracyjna zmodyfikowanej metody Newtona
def krok(x, r, f_val, fp_val):
    wynik = x - r * f_val / fp_val
    return wynik

# Parametry początkowe
x0 = 3.0  # Wartość początkowa
alpha = 7  # Zero funkcji
r = 45      # Krotność zera
margines = 1e-6
max_iterations = 100
iterations = 0

# Iteracyjna metoda Newtona
while iterations < max_iterations:
    f_val = f(x0, alpha, r)
    fp_val = f_pochodna(x0, alpha, r)
    print(f_val)
    print(fp_val)
    if abs(fp_val) < margines:
        print("Pochodna bliska zeru, brak zbieżności.")
        break

    x_next = krok(x0, r, f_val, fp_val)
    error = abs(x_next - alpha)

    print(f"n = {iterations + 1}, x = {x_next:.6f}, błąd = {error:.6e}")

    if error < margines:
        print(f"Osiągnięto zbieżność po {iterations + 1} iteracjach.")
        break

    x0 = x_next
    iterations += 1

if iterations == max_iterations:
    print("Nie osiągnięto zbieżności po maksymalnej liczbie iteracji.")