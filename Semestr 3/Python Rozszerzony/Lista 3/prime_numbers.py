from math import sqrt
from timeit import timeit
from tabulate import tabulate

def pierwsze_imperatywna(n):
    if n < 2:
        return []
    primes = []
    for i in range(2, n):
        is_prime = True
        for j in range(2, int(sqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(i)
    return primes

def pierwsze_skladana(n):
    return [i for i in range(2, n + 1) if all(i % j != 0 for j in range(2, int(sqrt(i)) + 1))]

def pierwsze_funkcyjna(n):
    return list(filter(lambda x : all(x % j != 0 for j in range(2, int(sqrt(x)) + 1)), [i for i in range(2, n + 1)]))

n_values = [n for n in range(10, 101, 10)]
results = []
for n in n_values:
    time_i = timeit(lambda : pierwsze_imperatywna(n), number=1000)
    time_s = timeit(lambda : pierwsze_skladana(n), number=1000)
    time_f = timeit(lambda : pierwsze_funkcyjna(n), number=1000)
    results.append([n, round(time_i, 8), round(time_s, 8), round(time_f, 8)])

table = tabulate(results, headers=["n", 'imperatywna', 'skladana', 'funkcyjna'], tablefmt='grid')
print(table)
print(f'Pierwsze imperatywnie: {pierwsze_imperatywna(100)}')
print(f'Pierwsze skladanie: {pierwsze_skladana(100)}')
print(f'Pierwsze funkcyjnie: {pierwsze_funkcyjna(100)}')
