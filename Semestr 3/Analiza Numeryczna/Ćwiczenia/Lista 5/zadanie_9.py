import mpmath
from mpmath import mp

# Ustawienie precyzji (np. 128 cyfr)
mp.dps = 128  # Liczba cyfr dziesiętnych


# Definicja funkcji f(x), jej pierwszej i drugiej pochodnej
def f(x):
    return x ** 3 - 2 * x - 5  # Przykładowa funkcja


def f_prime(x):
    return 3 * x ** 2 - 2  # Pochodna pierwsza funkcji


def f_double_prime(x):
    return 6 * x  # Pochodna druga funkcji

def f2(x):
    return x ** 2 + 3 * x + 1

def f_prime2(x):
    return 2 * x + 3

def f_double_prime2(x):
    return 2

import math

def f3(x):
    return x**3 + 17

def f_prime3(x):
    return 3*x**2

def f_double_prime3(x):
    return 6*x


# Metoda Olvera
def olvera_method(xn,f, f_prime, f_double_prime):
    fxn = f(xn)
    fxn_prime = f_prime(xn)
    fxn_double_prime = f_double_prime(xn)

    term1 = fxn / fxn_prime
    term2 = (fxn / fxn_prime) ** 2 * fxn_double_prime / (2 * fxn_prime)

    return xn - term1 - term2


# Przeprowadzanie iteracji
def find_root(x0, f, f_prime, f_double_prime, tol=1e-50, max_iter=100, ):
    xn = mp.mpf(x0)  # Startowa wartość (używamy typu mpmath)
    errors = []  # Lista do przechowywania błędów
    xn_values = [xn]  # Lista do przechowywania wartości x_n

    # Iteracje metody Olvera
    for i in range(max_iter):
        xn_next = olvera_method(xn, f, f_prime, f_double_prime)
        error = abs(xn_next - xn)  # Błąd jako różnica kolejnych przybliżeń
        errors.append(error)
        xn_values.append(xn_next)

        if error < tol:
            break

        xn = xn_next

    # Obliczanie rzędu zbieżności
    print("Iteracja | x_n                         | Błąd                         | Przybliżony rząd zbieżności p")
    for i in range(1, len(errors) - 1):
        # Obliczenie przybliżonego rzędu zbieżności
        p_approx = mpmath.log(abs(errors[i + 1]) / abs(errors[i])) / mpmath.log(abs(errors[i]) / abs(errors[i - 1]))
        print(f"{i + 1:>8} | {mp.nstr(xn_values[i], 25):<30} | {mp.nstr(errors[i], 22):<30} | {mp.nstr(p_approx, 10)}")


# Ustalamy początkowe przybliżenie
x0 = 2.0  # Przykładowa wartość początkowa
lista_x = [-5, 0, 2, 5, .6]
for x in lista_x:
    find_root(x, f, f_prime, f_double_prime)

print("\n\n\n\n")

for x in lista_x:
    find_root(x, f2, f_prime2, f_double_prime2)

print("\n\n\n\n")


# for x in lista_x:
#     find_root(x, f3, f_prime3, f_double_prime3)
