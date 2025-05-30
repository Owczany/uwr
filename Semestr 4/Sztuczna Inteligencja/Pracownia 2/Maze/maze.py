from collections import deque

INPUT_FILE = 'maze_input.txt'
OUTPUT_FILE = 'maze_output.txt'

def print_maze(maze: list[str]) -> None:
    '''
    Rysuje w konosoli wygląd labiryntu
    '''
    for row in maze:
        print(row)

def read_input_file(filename: str) -> list[str]:
    """
    Wczytuje plik tekstowy i zwraca listę linii bez znaków nowej linii.

    Args:
        filename (str): Ścieżka do pliku.

    Returns:
        list[str]: Lista linii jako stringi.
    """
    with open(filename, 'r') as f:
        return [c for c in [line.removesuffix('\n') for line in f.readlines()]]

def write_output_file(filename: str, path: list[str]) -> None:
    with open(filename, 'w') as f:
        if path:
            f.write("".join(path))
        else:
            f.write("Path doesn't exits!")

def positions(maze: list[str]):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 'S':
                s_pos = (y, x)
            elif maze[y][x] == 'G':
                g_pos = (y, x)
    return s_pos, g_pos


maze = read_input_file(INPUT_FILE)

s_pos, g_pos = positions(maze)
print(s_pos)
print(g_pos)

directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1)}

def move(pos, direction: str):
    dy, dx = directions[direction]
    y, x = pos
    new_y, new_x = y + dy, x + dx
    if maze[new_y][new_x] != '#':
        return (new_y, new_x)
    return (y, x)

def solve_bfs() -> (list[str] | None):
    visited = set()
    visited.add(s_pos)

    queue = deque([(s_pos, [])])

    while queue:
        curr_pos, moves = queue.popleft()
        print(moves)

        if curr_pos == g_pos:
            return moves

        for dir in ['U', 'D', 'L', 'R']:
            new_pos = move(curr_pos, dir)
            if new_pos not in visited:
                queue.append((new_pos, moves + [dir]))
                visited.add(new_pos)

    return None   


write_output_file(OUTPUT_FILE, solve_bfs())
print_maze(maze)
print(solve_bfs())