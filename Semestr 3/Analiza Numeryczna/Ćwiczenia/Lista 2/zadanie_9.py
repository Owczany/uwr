from math import sqrt

def ciag1(n, x1=2):
    if n == 1:
        return x1
    
    term = x1

    for k in range(1, n + 1):
        term = 2**k * sqrt(2 * (1 - sqrt(1 - (term / 2 ** k) ** 2)))
    return term

def ciag2(n, x1=2):
    if n == 1:
        return x1
    
    term = x1

    for k in range(1, n + 1):
        innerSqrt = sqrt(1 - (term / 2**k)**2)
        term = term * sqrt(2 / (1 + innerSqrt))
    return term

print(ciag1(1000, 2))
print(ciag2(1000, 2))
