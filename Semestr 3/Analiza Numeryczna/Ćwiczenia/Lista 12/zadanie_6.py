import numpy as np

def f1(x):
    return np.cos(x)

def f2(x):
    return x**(-1)

def f3(x):
    return 1 / (1 + (x ** 2))

def numerical_integral(a, b, n, f):
    h = (b - a) / n
    nodes = [a + i * h for i in range(n + 1)]  # Równo odległe węzły
    A = newton_cotes_weights(nodes, a, b)  # Oblicz współczynniki Ak
    res = 0
    for k, node in enumerate(nodes):
        res += A[k] * f(node)
    return res

def newton_cotes_weights(nodes, a, b):
    def get_products(nodes):
        polynomial = [1]
        for xi in nodes:
            new_polynomial = [0] * (len(polynomial) + 1)
            for i in range(len(polynomial)):
                new_polynomial[i] += polynomial[i] * -xi
                new_polynomial[i + 1] += polynomial[i]
            polynomial = new_polynomial
        return polynomial

    products = get_products(nodes)

    def horner_division(polynomial, c):
        new_polynomial = [0] * (len(polynomial) - 1)
        new_polynomial[-1] = polynomial[-1]
        for i in range(len(new_polynomial) -2, -1, -1):
            new_polynomial[i] = new_polynomial[i + 1] * c + polynomial[i]
        return new_polynomial

    def derivative_at_node(nodes, k):
        result = 1
        for i in range(len(nodes)):
            if i != k:
                result *= (nodes[k] - nodes[i])
        return result

    weights = [0] * len(nodes)
    mid = len(weights) // 2
    for k in range(mid + 1):  # Obliczamy tylko połowę współczynników
        polynomial = horner_division(products, nodes[k])
        derivative = derivative_at_node(nodes, k)
        integral = 0
        for i, factor in enumerate(polynomial):
            integral += factor * ((b ** (i + 1) - a ** (i + 1)) / (i + 1))
        weight = integral / derivative
        weights[k] = weight
        weights[-(k + 1)] = weight
    return weights

def main():
    for n in range(2, 50):
        print(f"n = {n}")
        print(f"Integral of f1 on [-3, 4]: {numerical_integral(-3, 4, n, f1):.6f}")
        print(f"Integral of f2 on [1, 2]: {numerical_integral(1, 2, n, f2):.6f}")
        print(f"Integral of f3 on [-5, 5]: {numerical_integral(-5, 5, n, f3):.6f}")

if __name__ == '__main__':
    main()
