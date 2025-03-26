def solve_sudoku(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    def is_valid(num, r, c, matrix):
        # Sprawdź wiersz i kolumnę
        for i in range(num_rows):
            if matrix[r][i] == num or matrix[i][c] == num:
                return False
        # Sprawdź podsiatkę 3x3
        start_row, start_col = 3 * (r // 3), 3 * (c // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if matrix[i][j] == num:
                    return False
        return True

    def dfs(start_index, matrix):
        if start_index == num_rows * num_rows:
            yield matrix
            return
        
        row = start_index // num_rows 
        col = start_index % num_cols
        
        if matrix[row][col]:
            yield from dfs(start_index + 1, matrix)
        else:
            for digit in range(1, 10):
                if is_valid(str(digit), row, col, matrix):
                    matrix[row][col] = str(digit)
                    yield from dfs(start_index + 1, matrix)
                    matrix[row][col] = ''

    yield from dfs(0, matrix)

# Testy

# No Solution
no_solution_sudoku = [ 
    ['', '6', '5', '', '', '7', '', '1', ''],
    ['', '', '', '9', '1', '5', '6', '', ''],
    ['', '9', '', '', '', '', '', '5', ''],
    ['', '', '', '', '4', '', '7', '2', ''],
    ['3', '7', '', '', '', '', '', '', ''],
    ['6', '', '9', '', '7', '', '', '', ''],
    ['9', '', '', '7', '', '', '5', '', ''],
    ['5', '8', '', '1', '3', '', '', '7', ''],
    ['', '', '7', '3', '', '', '', '', '2'],
]

# One Solution
one_solution_sudoku = [ 
    ['', '6', '5', '', '', '7', '', '1', ''],
    ['', '', '', '9', '1', '5', '6', '', ''],
    ['', '9', '', '', '', '', '', '5', ''],
    ['', '', '', '', '4', '', '7', '2', ''],
    ['3', '7', '', '', '', '', '', '', ''],
    ['6', '', '9', '', '7', '', '', '', ''],
    ['9', '', '', '7', '', '', '5', '', ''],
    ['5', '8', '', '1', '3', '', '', '7', ''],
    ['', '', '7', '', '', '', '', '', '2'],
]

# Few Solutions
few_solutions_sudoku = [ 
    ['', '6', '5', '', '', '7', '', '1', ''],
    ['', '', '', '9', '1', '5', '6', '', ''],
    ['', '9', '', '', '', '', '', '5', ''],
    ['', '', '', '', '4', '', '', '2', ''],
    ['3', '7', '', '', '', '', '', '', ''],
    ['6', '', '9', '', '7', '', '', '', ''],
    ['9', '', '', '7', '', '', '5', '', ''],
    ['5', '8', '', '1', '3', '', '', '7', ''],
    ['', '', '', '', '', '', '', '', '2'],
]

# A lot of Solutions
lot_solutions_sudoku = [ 
    ['', '6', '5', '', '', '7', '', '1', ''],
    ['', '', '', '9', '', '', '6', '', ''],
    ['', '9', '', '', '', '', '', '5', ''],
    ['', '', '', '', '4', '', '7', '2', ''],
    ['3', '7', '', '', '', '', '', '', ''],
    ['', '', '9', '', '7', '', '', '', ''],
    ['', '', '', '7', '', '', '5', '', ''],
    ['', '8', '', '1', '3', '', '', '7', ''],
    ['', '', '', '', '', '', '', '', '2'],
]

# Wyświetlanie wyników
for solution in solve_sudoku(lot_solutions_sudoku):
    for row in solution:
        print(row)
    print()
