import numpy as np
import matplotlib.pyplot as plt

# Funkcja do generowania wartości zmiennopozycyjnej
def floating_point_value(sign, b2, b3, b4, b5, exponent_sign, c):
    mantissa = 0.5 + 0.25 * b2 + 0.125 * b3 + 0.0625 * b4 + 0.03125 * b5
    exponent = (2 ** ((-1)**exponent_sign * c))
    return sign * mantissa * exponent

# Wszystkie możliwe kombinacje bitów
values = []
for sign in [-1, 1]:
    for b2 in [0, 1]:
        for b3 in [0, 1]:
            for b4 in [0, 1]:
                for b5 in [0, 1]:
                    for exponent_sign in [0, 1]:
                        for c in [0, 1]:
                            x = floating_point_value(sign, b2, b3, b4, b5, exponent_sign, c)
                            values.append(x)

# Sortowanie wartości
values = sorted(values)

# Rysowanie wykresu
print(values)
plt.figure(figsize=(300, 6))
plt.scatter(values, np.zeros_like(values), c='blue', marker='x')
plt.title('Rozkład liczb zmiennopozycyjnych')
plt.xlabel('Wartości')
plt.grid(True)
plt.show()

# Znalezienie najmniejszego i największego x
A = min(values)
B = max(values)

print(A)
print(B)
