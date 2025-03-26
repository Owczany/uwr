import math
def krok(x, m):
    wynik = 0.5 * (x + m / x)
    return wynik

def newton(m, c, x0):
    e = 100000000
    # x0 = 1
    i = 0
    # m = 0.8
    # c = 2
    a = m * pow(2, c)
    max_iterations = 100  # Maksymalna liczba iteracji, aby zapobiec nieskończonej pętli
    print(f"a = {a}")
    # Iteracyjny proces dla obliczenia sqrt(m)
    while e > 10**(-6) and i < max_iterations:
        i += 1
        x = krok(x0, m)
        e = abs(x - x0)
        x0 = x
    print('Iterations:', i)
    # Końcowe obliczenie sqrt(a) = sqrt(m) * 2^(c/2)
    if e <= 10**(-6):
        sqrt_a = x0 * pow(2, c / 2)
        print("Ostateczny wynik sqrt(a):", sqrt_a)
        print("porównanie z biblioteczną funkcją:", math.sqrt(a))
    else:
        print("Metoda nie zbiega się po", max_iterations, "iteracjach")

tests = [(m, c, x0) for m in [0.5, 0.6, 0.7, 0.8, 0.9] for c in range(0, 10) for x0 in range(1, 100, 10)]

for m, c, x0 in tests:
    print(f'm = {m}, c = {c}, x0 = {x0}')
    newton(m, c, x0)