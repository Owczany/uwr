import random

MAX_N = 1_000_000
MIN_COORD = -10**7
MAX_COORD = 10**7

def generate_unique_points(n):
    seen = set()
    points = []

    while len(points) < n:
        x = 7
        y = random.randint(MIN_COORD, MAX_COORD)
        if (x, y) not in seen:
            seen.add((x, y))
            points.append((x, y))

    return points

def save_to_file(points, filename="test_max.txt"):
    with open(filename, "w") as f:
        f.write(f"{len(points)}\n")
        for x, y in points:
            f.write(f"{x} {y}\n")

if __name__ == "__main__":
    print("Generating points...")
    points = generate_unique_points(MAX_N)
    print("Saving to file...")
    save_to_file(points)
    print("Done. Test saved as 'test_max.txt'")
