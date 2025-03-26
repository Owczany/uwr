def inverse_approximation(R, x0, tolerance=1e-16, max_iterations=1000):
    """
    Parametry:
    R : float - liczba, której odwrotność chcemy przybliżyć
    x0 : float - początkowe przybliżenie dla 1/R
    tolerance : float - oczekiwana dokładność wyniku
    max_iterations : int - maksymalna liczba iteracji żeby się nie zapętliło

    Zwraca:
    xn : float - przybliżona wartość 1/R
    n : int - liczba iteracji potrzebna do osiągnięcia oczekiwanej dokładności
    """
    xn = x0
    for n in range(max_iterations):
        xn_next = xn * (2 - xn * R)

        if abs(xn_next - xn) < tolerance:
            return xn_next, n + 1

        xn = xn_next

    return xn, max_iterations  # Jeśli nie osiągnie tolerancji, zwraca wynik po max_iterations


# Testowanie dla różnych wartości R i x0
results = []
test_cases = [(R, x0) for R in [2, 10, 50, 100, 1000] for x0 in [0.1, 0.5, 1 / R * 0.9]]

for R, x0 in test_cases:
    approximation, iterations = inverse_approximation(R, x0)
    results.append((R, x0, approximation, iterations))

# Wyświetlenie wyników
for R, x0, approximation, iterations in results:
    print(f"R = {R:<5}, x0 = {x0:<20}, Wynik = {approximation:<20}, Liczba iteracji = {iterations}")