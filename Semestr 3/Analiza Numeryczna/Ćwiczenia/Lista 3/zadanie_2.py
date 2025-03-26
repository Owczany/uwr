from math import sqrt

def f(x, a, b, c):
    return a * x**2 + b * x + c

def kwadratowa(a, b, c):
    delta = sqrt(b**2 - 4*a*c)

    if delta < 0:
        return (None, None)
    
    x1 = ( -b - delta ) / (2 * a)
    x2 = ( -b + delta ) / (2 * a)
    return (x1, x2)

def kwadratowa_fix(a, b, c):
    delta = sqrt(b**2 - 4*a*c)

    if delta < 0:
        return (None, None)

    if b > 0:
        x1 = ( -b - delta ) / (2 * a)
    else:
        x1 = ( -b +  delta ) / (2 * a)
    if x1 != 0:
        x2 = c / (a * x1)
    else:
        x2 = - b / a

    return (x1, x2)


x = 0
y = 9
z = 0
a = 1
b = 1
c = 1

x1, x2 = kwadratowa(1 * 10**x, 1 * 10**y, 1 * 10**z)
print((x1, x2))
print(f(x1, 1 * 10**x, 1 * 10**y, 1 * 10**z))
print(f(x2, 1 * 10**x, 1 * 10**y, 1 * 10**z))
x1, x2 = kwadratowa_fix(1 * 10**x, 1 * 10**y, 1 * 10**z)
print((x1, x2))
print(f(x1, 1 * 10**x, 1 * 10**y, 1 * 10**z))
print(f(x2, 1 * 10**x, 1 * 10**y, 1 * 10**z))