import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.polynomial import Polynomial

# Funkcja f(t) z teorii
def f(t):
    return 6.02 * (t + 3.2) * (t - 0.02) * (t + 1.7)

# Wczytanie danych z pliku
data = np.loadtxt('punkty.csv', delimiter=',')
t_data, y_data = data[:, 0], data[:, 1]

# (a) Wykres funkcji f(t) i punktów X
t_range = np.linspace(-5, 3, 500)
f_values = f(t_range)

plt.figure(figsize=(12, 6))
plt.plot(t_range, f_values, label='Funkcja $f(t)$', color='blue')
plt.scatter(t_data, y_data, color='red', label='Punkty X', alpha=0.7)
plt.title('Wykres funkcji $f(t)$ i punkty X')
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.legend()
plt.grid()
plt.show()

# (b) Wielomian interpolacyjny
def lagrange_interpolation(x, t_data, y_data):
    """Wielomian Lagrange'a."""
    def l(i, x):
        result = 1
        for j in range(len(t_data)):
            if i != j:
                result *= (x - t_data[j]) / (t_data[i] - t_data[j])
        return result

    result = 0
    for i in range(len(t_data)):
        result += y_data[i] * l(i, x)
    return result

# Wartości interpolacji
lagrange_values = [lagrange_interpolation(t, t_data, y_data) for t in t_range]


plt.figure(figsize=(12, 6))
plt.plot(t_range, f_values, label='Funkcja $f(t)$', color='blue')
plt.plot(t_range, lagrange_values, label='Interpolacja Lagrange\'a', color='red')
plt.scatter(t_data, y_data, color='black', label='Punkty X', alpha=0.7)
plt.title('Wielomian interpolacyjny Lagrange\'a')
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.legend()
plt.grid()
plt.show()


def least_squares_fit(t, y, degree):
    # Liczba punktów
    n = len(t)

    # Tworzenie macierzy A (każdy wiersz: [1, t_i, t_i^2, ..., t_i^degree])
    A = np.zeros((n, degree + 1))
    for i in range(n):
        for j in range(degree + 1):
            A[i, j] = t[i] ** j

    # Tworzenie macierzy transponowanej A^T
    A_T = np.zeros((degree + 1, n))
    for i in range(degree + 1):
        for j in range(n):
            A_T[i, j] = A[j, i]

    # Obliczanie macierzy A^T * A
    ATA = np.zeros((degree + 1, degree + 1))
    for i in range(degree + 1):
        for j in range(degree + 1):
            ATA[i, j] = sum(A_T[i, k] * A[k, j] for k in range(n))

    # Obliczanie macierzy A^T * y
    ATy = np.zeros(degree + 1)
    for i in range(degree + 1):
        ATy[i] = sum(A_T[i, k] * y[k] for k in range(n))

    # Rozwiązywanie równania (ATA * coeffs = ATy) metodą eliminacji Gaussa
    coeffs = np.zeros(degree + 1)
    for i in range(degree + 1):
        # Skalowanie wiersza
        factor = ATA[i, i]
        for j in range(degree + 1):
            ATA[i, j] /= factor
        ATy[i] /= factor

        # Zerowanie poniżej
        for k in range(i + 1, degree + 1):
            factor = ATA[k, i]
            for j in range(degree + 1):
                ATA[k, j] -= factor * ATA[i, j]
            ATy[k] -= factor * ATy[i]

    # Rozwiązywanie układu (tylne podstawianie)
    for i in range(degree, -1, -1):
        coeffs[i] = ATy[i]
        for j in range(i + 1, degree + 1):
            coeffs[i] -= ATA[i, j] * coeffs[j]

    return coeffs

plt.figure(figsize=(14, 8))
plt.plot(t_range, f_values, label='Funkcja $f(t)$', color='blue')

for n in range(2, 16):
    # Konstrukcja wielomianu optymalnego
    approx_poly = lambda t: sum(c * t ** i for i, c in enumerate(least_squares_fit(t_data, y_data, n)))
    approx_values = [approx_poly(t) for t in t_range]
    
    # Rysowanie wielomianu optymalnego
    plt.plot(t_range, approx_values, label=f'Wielomian optymalny (stopień {n})', alpha=0.7)

plt.scatter(t_data, y_data, color='red', label='Punkty X', alpha=0.7)
plt.title('Wielomiany optymalne w sensie średniokwadratowym')
plt.xlabel('$t$')
plt.ylabel('$y$')
plt.legend()
plt.grid()
plt.show()
