import matplotlib.pyplot as plt
import numpy as np

T = [0, 10, 20, 30, 40, 80, 90, 95]
S = [68.0, 67.1, 66.4, 65.6, 64.6, 61.8, 61.0, 60.0]

a = -0.08
b = 67.96

t = np.linspace(0, 95, 1000)
s = [a*ti + b for ti in t]


w1 = 0
w2 = 0
o1 = 0
o2 = 0
n = len(T)
for i in range(n):
    w1 += T[i]**2
    w2 += T[i]
    o1 += S[i] * T[i]
    o2 += S[i]

print(w1)
print(w2)
print(o1)
print(o2)

plt.scatter(T, S)
plt.plot(t, s)
plt.show()
