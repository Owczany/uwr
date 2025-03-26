from math import sqrt

# Źle z zadania
def f1(x):
    return 8096 * (sqrt(x ** 13 + 4) - 2) / x ** 14

# Poprawne
def f2(x):
    return 8096 / (x * (sqrt((x ** 13) + 4) + 2))

# Jak korzystamy z pierwszej metody dochodzi do utraty precyzji bo odejmujemy od siebie dwie bardzo małe liczby

print(f1(0.001))
print(f2(0.001))
