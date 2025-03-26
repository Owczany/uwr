import math

def taylor_sin(x, tolerance=1e-10):
    x = x % (2 * math.pi)
    
    term = x  # Pierwszy wyraz szeregu (dla n = 0)
    sin_x = term
    n = 1
    
    while abs(term) > tolerance:
        term = -term * (x*x) / ((2*n) * (2*n + 1))
        sin_x += term
        n += 1
    print(n)
    return sin_x

print(math.sin(6392019301))
print(taylor_sin(6392019301))