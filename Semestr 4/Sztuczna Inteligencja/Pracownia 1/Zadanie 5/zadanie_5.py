import random

# Plik wejściowy i wyjściowy
INPUT_FILE = 'zad5_input.txt'
OUTPUT_FILE = 'zad5_output.txt'

def read_input_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    x, y = map(int, lines[0].split())

    x_lines = [int(line) for line in lines[1:x + 1]]
    y_lines = [int(line) for line in lines[x + 1:x + 1 + y]]

    return x, y, x_lines, y_lines

def write_output_file(filename, grid):
    """Zapisuje wyniki do pliku."""
    with open(filename, 'w') as f:
        for row in grid:
            f.write(''.join(row) + '\n')

def count_blocks(line):
    """Zlicza liczbę bloków jedynek w tablicy."""
    prev = line[0]
    count = 1 if prev == '#' else 0
    for i in range(1, len(line)):
        if prev == '.' and line[i] == '#':
            count += 1
        prev = line[i]
    return count

def check_line(line, num):
    return count_blocks(line) == 1 and line.count('#') == num

def generate_random_grid(x, y):
    return [['#' if random.random() > 0.5 else '.' for _ in range(y)] for _ in range(x)]

def solve(x, y, x_lines, y_lines, max_iterations=5000000, restart_threshold = 5000):
    grid = generate_random_grid(x, y)
    
    for iteration in range(max_iterations):
        incorrect_rows = [i for i in range(x) if not check_line(grid[i], x_lines[i])]
        incorrect_cols = [j for j in range(y) if not check_line([grid[i][j] for i in range(x)], y_lines[j])]
        
        # Dobrze rozwiązany Nonogram
        if not incorrect_rows and not incorrect_cols:
            return grid
        
        # Restart jeśli przez dłuższy czas nie ma poprawy
        if iteration % restart_threshold == 0:
            grid = generate_random_grid(x, y)
            continue
        
        # Wybierz losowy wiersz lub kolumnę do poprawienia
        if incorrect_rows:
            row = random.choice(incorrect_rows)
            col = min(range(y), key=lambda j: improvement_assesment(grid, row, j, x_lines, y_lines))
        elif incorrect_cols:
            col = random.choice(incorrect_cols)
            row = min(range(x), key=lambda i: improvement_assesment(grid, i, col, x_lines, y_lines))
        
        # Zamiana wartości w wybranym pikselu
        grid[row][col] = '#' if grid[row][col] == '.' else '.'
        

        if random.random() < 0.03:
            r, c = random.randint(0, x - 1), random.randint(0, y - 1)
            grid[r][c] = '#' if grid[r][c] == '.' else '.'
    return grid

def improvement_assesment(grid, row, col, x_lines, y_lines):
    """Oblicza, jak bardzo poprawi się dopasowanie po zmianie piksela"""
    original_value = grid[row][col]

    # Zamieniamy piksel
    grid[row][col] = '#' if original_value == '.' else '.'

    row_correct = check_line(grid[row], x_lines[row])
    col_correct = check_line([grid[i][col] for i in range(len(grid))], y_lines[col])

    # Przywracamy oryginalny stan
    grid[row][col] = original_value

    #Im mniej tym lepiej
    return int(not row_correct) + int(not col_correct)


def main():
    x, y, x_lines, y_lines = read_input_file(INPUT_FILE)
    solution = solve(x, y, x_lines, y_lines)
    write_output_file(OUTPUT_FILE, solution)

    
    
    write_output_file(OUTPUT_FILE, solution)
    
    

if __name__ == '__main__':
    main()