from math import pi
from numpy import sin

# A)
def a(x):
    return (x - 2024)**5

print(a(2024.0000000000000000000001))

def b(x):
    return sin(-8*x)

print(b(pi*1000))

def c(x):
    return (2024 + x**8) ** -2

print(c(1000))