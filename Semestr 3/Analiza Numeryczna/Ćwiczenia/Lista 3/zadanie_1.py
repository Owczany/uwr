from math import sqrt, e, pi
from numpy import arcsin, cos

# A)
# dla x >=0 jest dobry
def a(x):
    return 1 / (x**5 + sqrt(x**10 + 2024))

# poprawiony
def A(x):
    return (x**5 - sqrt(x**10 + 2024)) / -2024

# Testy
# print(a(-100))
print(A(-100))

# B)
# Problem dla x -> 0
def b(x):
    return (10**8) * (e**x - e**(2*x))

def B(x):
    term1 = x
    term2 = 2 * x
    s = term2 - term1
    for n in range(2, 100):
        term1 = term1 * x / n
        term2 = 2 * term2 * x / n
        s += (term2 - term1)
    return -(10**8)*(x + (3 *  x**2 / 2) + (7 * x**3 / 6))

# Testy
print(b(0.0000000000000000000000000000001))
print(B(0.0000000000000000000000000000001))

# C)
# Taylor Znowu
def c(x):
    return 6 * (arcsin(x) - x) / (x**3)

def C(x):
    term = x**3 / 6
    s = term

    for n in range(2, 100):
        term = term * (x * x) * (2 * n) * (2 * n + 1) / (4**n * (n * (n - 1))**2 * (2 * n + 1))
        s += term

    return 6 * s / x**3

print(c(0.0000000000000000000000000000001))
print(C(0.0000000000000000000000000000001))

# D)

def d(x):
    return 4 * (cos(x)**2) - 1

def D(x):
    term = -x**2 / 2
    s = term

    for n in range(2, 100):
        term = -term * (x * x) / ((2 * n) * (2 * n - 1))
        s += term
    
    return (2 * cos(x) + 1) * (2 * s + 1)

def d_fix(x):
    return (2 * cos(x) + 1) * ( ((1 / 2) - (sqrt(3) / 2) * (x - (pi / 3)) - (1 / 4) * (x - (pi / 3))**2 + (sqrt(3) / 12) * (x - (pi / 3))**3) - 1)

print(d((pi + 0.0000000000001) / 3))
print(D((pi + 0.0000000000001) / 3))
print(d_fix((pi/ 3)))