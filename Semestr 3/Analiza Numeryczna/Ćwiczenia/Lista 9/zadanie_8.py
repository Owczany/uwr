import matplotlib.pyplot as plt
import numpy as np
import math

points = [(39.5, 10.5), (30, 20), (6, 6), (13, -12), (63, -12.5), (18.5, 17.5), (48, 63), (7, 25.5), (48.5, 49.5), (9, 19.5), (48.5, 35.5), (59, 32.5), (56, 20.5)]

wages = [1, 2, 3, 2.5, 6, 1.5, 5, 1, 2, 1, 3, 5, 1]

t = np.linspace(0, 1, 1000)

def bernsteinPolynomial(x, k, n):
    return math.comb(n, k) * pow(x, k) * pow((1 - x), (n - k))

x_axis = []
y_axis = []

for item in t:
    dol = 0
    x = 0
    y = 0
    n = len(points) - 1
    for i in range(len(points)):
        dol += wages[i] * bernsteinPolynomial(item, i, n)
        x += wages[i] * points[i][0] * bernsteinPolynomial(item, i, n)
        y += wages[i] * points[i][1] * bernsteinPolynomial(item, i, n)
    x_axis.append(x / dol)
    y_axis.append(y / dol)


plt.figure(figsize=(10, 6))
plt.plot(x_axis, y_axis, label="Krzywa Béziera")
plt.scatter(*zip(*points), color="red", label="Punkty kontrolne")
plt.legend()
plt.title("Wymierna krzywa Béziera")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid()
plt.show()
