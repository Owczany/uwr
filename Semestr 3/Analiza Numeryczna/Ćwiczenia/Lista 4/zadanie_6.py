def krok(x, a):
    wynik = x * ((3 - a * x * x) / 2)
    return wynik

e = 100000000
x0 = .12
i = 0
a = 4
max_iterations = 100  # Maksymalna liczba iteracji, aby zapobiec nieskończonej pętli

while e > 10**(-6) and i < max_iterations:
    i += 1
    x = krok(x0, a)
    e = abs(x - x0)
    x0 = x
    print(f"n = {i} x = {x} e = {e}")

if e <= 10**(-6):
    print("Ostateczny wynik x0:", x0)
else:
    print("Metoda nie zbiega się po", max_iterations, "iteracjach")