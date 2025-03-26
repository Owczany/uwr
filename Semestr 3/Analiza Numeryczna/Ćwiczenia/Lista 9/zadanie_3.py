import matplotlib.pyplot as plt
import numpy as np
import math

# Funkcja Bernsteina
def bernsteinPolynomial(x, k, n):
    return math.comb(n, k) * (x ** k) * ((1 - x) ** (n - k))

# Punkty kontrolne
points = [-1, 3, 0.1, 100, 20]
n = len(points) - 1  # Stopień wielomianu

# Wykres wielomianu
t = np.linspace(0, 1, 1000)
y_axis = []

for item in t:
    y = 0
    for i in range(len(points)):
        y += points[i] * bernsteinPolynomial(item, i, n)
    y_axis.append(y)

# Punkty kontrolne (k/n, a_k)
control_points = [(k / n, points[k]) for k in range(len(points))]

# Rysowanie
plt.figure(figsize=(10, 6))
plt.plot(t, y_axis, label="Wykres wielomianu $p(t)$", color="blue")
plt.scatter(*zip(*control_points), color="red", label="Punkty kontrolne $(k/n, a_k)$")
plt.fill(*zip(*control_points), color="red", alpha=0.2, label="Otoczka wypukła")
plt.legend()
plt.title("Wielomian Béziera i otoczka wypukła punktów kontrolnych")
plt.xlabel("t")
plt.ylabel("p(t)")
plt.grid()
plt.show()
