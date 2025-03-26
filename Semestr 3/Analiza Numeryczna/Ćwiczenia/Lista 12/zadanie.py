import math
# from Lagrange import Ln
import matplotlib.pyplot as plt

def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)
    
def horner(P, k):
    n = len(P) - 2
    Pk = [0] * (n + 2)
    Pk[n + 1] = P[n + 1]

    for i in range(n, 0 , -1):
        Pk[i] = Pk[i + 1] * k + P[i]

    assert Pk[0] == 0
    Pk = Pk[1:]

    return Pk

def integral(Pk, n): # calka z wielomianu Pk od 0 do n
    x = n

    I = 0
    for i in range(n + 1):
        I += Pk[i] * x / (i + 1)
        x *= n

    return I
        
def polynomial(n): # t(t-1)(t-2)...(t-n)
    P = [0] * (n + 2)
    P[0] = 1
    maxIndex = 0

    for j in range(n + 1):
        for index in range(maxIndex + 1, -1, -1):
            if index == 0:
                P[index] = -j * P[index]
            else:
                P[index] = P[index - 1] - j * P[index]
        maxIndex += 1

    return P

def NCFactors(n, h):
    m = (n + 1) // 2
    factorial_n = factorial(n)
    As = [0] * (n + 1)

    factorial_k = 1
    for k in range(n - m + 1):
        if k == 0:
            factorial_k = 1
        else:
            factorial_k *= k
            factorial_n /= (n - k + 1)

        sign = 1 if (n - k) % 2 == 0 else -1

        As[k] = sign * h / (factorial_k * factorial_n)
        As[n - k] = As[k]

    # teraz calka 

    P = polynomial(n)

    # t^0 + t^1 + t^2 + ... + t^(n+1)

    for k in range(n - m + 1):
        # Pk = P/(t-k) schematem Hornera w O(n)
        Pk = horner(P, k)
        Ik = integral(Pk, n)
        As[k] *= Ik
        if k != n - k:
            As[n - k] *= Ik

    return As

def NewtonCotes(f, a, b, n):
    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    As = NCFactors(n, h)

    Q = 0
    for i in range(n + 1):
        Q += As[i] * f(xs[i])

    return Q

def nodesF (n, f, a, b):
    h = (b - a) / n
    xs = [a + i * h for i in range(n + 1)]
    ys = [f(x) for x in xs]

    return xs, ys


#print (horner([4, -4, 1], 2))

P = polynomial(5)
#print(P)
    
Ptwo = horner(P, 2)
#print(Ptwo)

I = integral(Ptwo, 5)
#print(I)

# cos
def f1(x):
    return math.cos(x)

# x^-1
def f2(x):
    return 1 / x

# 1 / (1 + x^2)
def f3(x):
    return 1 / (1 + x * x)

for n in range (2, 26):
    print("n = ", n)
    print("\t1. ", NewtonCotes(f1, -3, 4, n))
    print("\t2. ", NewtonCotes(f2, 1, 2, n))
    print("\t3. ", NewtonCotes(f3, 0, 5, n))
    print()