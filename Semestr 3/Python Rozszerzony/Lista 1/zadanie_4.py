import random
import math

# Symulacja z przyblieniem
def simulation(ep):
    pi = 0
    shots = 0
    hits = 0
    while abs(math.pi - pi) > ep:
        shots += 1
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if (x**2 + y**2 < 1):
            hits += 1
        pi = 4 * hits / shots
        print(f"Trafionych {hits} z {shots}")
    return pi

print(f"Końcowy wynik: {simulation(0.0001)}") 
