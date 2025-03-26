import numpy as np
import math

# Definicja funkcji f(x)
def f_double(x):
    return 1518 * (2 * x - math.sin(2 * x)) / (x ** 3)

def f_single(x):
    # Zastosowanie arytmetyki single precision (32-bitowej) za pomocą NumPy
    x_single = np.float32(x)
    result = np.float32(1518) * (np.float32(2) * x_single - np.sin(np.float32(2) * x_single)) / (x_single ** np.float32(3))
    return result

# Obliczenia dla i = 11, 12, ..., 20
for i in range(11, 21):
    x = 10 ** (-i)
    double_precision_result = f_double(x)
    single_precision_result = f_single(x)
    print(f"x = 10^(-{i})")
    print(f"Double precision: {double_precision_result}")
    print(f"Single precision: {single_precision_result}")
    print("-" * 50)

# Wniosek wyniki są tragiczne i nie zgadzają się z rzeczywistością