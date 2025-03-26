import math

def taylor_sin(x, n = 5):
    x = x % (2 * math.pi)
    n = max(n, 2)
    term = 8/6  # Pierwszy wyraz szeregu (dla n = 0)
    sin_x = term
    n = 1
    
    for n in range(2, n): 
        term = -term * (x*x) / ((2*n) * (2*n + 1))
        sin_x += term
    return sin_x

def f(x):
    return 1518 * taylor_sin(x, 20)

for i in range(11, 21):
    print(f(10**-i))
print(f(0.1))