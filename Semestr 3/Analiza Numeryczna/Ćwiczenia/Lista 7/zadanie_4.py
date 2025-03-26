import matplotlib.pyplot as plt
import numpy as np

x_interval = np.linspace(-1, 1, 1000) # Próbkowanie 1000 puntków na przedziale [-1; 1]

# p(n+1)
def get_polynomial(x_interval, data):
    res = []
    for x in x_interval:
        term = 1
        for xk in data:
            term *= (x - xk)
        res.append(term)
    return res

def get_chebyshev_nodes(n, a=-1, b=1):
    return np.array([((a + b) / 2) + ((b - a) / 2) * np.cos((2 * k + 1) * np.pi / (2 * n)) for k in range(n)])


for n in range(4, 21):
    # Same distance nodes
    same_distance_nodes = np.linspace(-1, 1, n + 1)
    p_same_distance = get_polynomial(x_interval, same_distance_nodes)

    # Chebyshev nodes
    chebyshev_nodes = get_chebyshev_nodes(n + 1)
    p_chebyshev = get_polynomial(x_interval, chebyshev_nodes)

    plt.figure(figsize=(10,6))
    plt.plot(x_interval, p_same_distance, color='blue', label='Równomiernie wybrane węzły')
    plt.plot(x_interval, p_chebyshev, linestyle='--' , color='red' , label='Węzły Czybyszewa')
    plt.title(f"Wielomian dla n = {n}")
    plt.xlabel("x")
    plt.ylabel(f"P[{n+1}](x)")
    plt.axhline()
    plt.grid()
    plt.legend()
    plt.show()

# Nie występuje taki duzy efekt Roundiego

