import matplotlib.pyplot as plt
import numpy as np
from numpy import sin, cos, pi

t = [0, 2, 4, 6, 8, 10]
H = [1, 1.6, 1.4, 0.6, 0.2, 0.8]

h0 = 0.9333
a1 = 0.5773
a2 = 0.2666
x_axis = np.linspace(0, 10, 1000)
y_axis = [h0 + a1 * np.sin(np.pi * i / 6) + a2 * np.cos(np.pi * i / 6) for i in x_axis]

plt.scatter(t, H)
plt.plot(x_axis, y_axis)
plt.show()

# Obliczenia
# o1 = o2 = o3 = 0
# w1 = w2 = w3 = 0
# u1 = u2 = u3 = 0
# v1 = v2 = v3 = 0

# for k in range(len(t)):
#     o1 += H[k]
#     o2 += sin(pi * t[k] / 6) * H[k]
#     o3 += cos(pi * t[k] / 6) * H[k]

#     w1 += 1
#     w2 += sin(pi * t[k] / 6)
#     w3 += cos(pi * t[k] / 6)

#     u1 += sin(pi * t[k] / 6)
#     u2 += (sin(pi * t[k] / 6))**2 
#     u3 += cos(pi * t[k] / 6) * sin(pi * t[k] / 6)

#     v1 += cos(pi * t[k] / 6)
#     v2 += cos(pi * t[k] / 6) * sin(pi * t[k] / 6)
#     v3 += (cos(pi * t[k] / 6))**2

# print(o1)
# print(o2)
# print(o3)

# print(w1)
# print(w2)
# print(w3)

# print(u1)
# print(u2)
# print(u3)

# print(v1)
# print(v2)
# print(v3)