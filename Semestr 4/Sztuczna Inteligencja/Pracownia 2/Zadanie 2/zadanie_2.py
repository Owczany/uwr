from collections import deque

INPUT_FILE = 'zad2_input.txt'
OUTPUT_FILE = 'zad2_output.txt'

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
    
def write_output_file(filename: str) -> None:
    pass

maze = read_input_file(INPUT_FILE)

def get_possitions(maze: list[str]):
    s_pos = set()
    g_pos = set()
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 'S':
                s_pos.add((y, x))
            elif maze[y][x] == 'G':
                g_pos.add((y, x))
    return s_pos, g_pos


#####

def solve():
    visited = set()
    # state = frozenset(s_pos)
    visited.add()

    queue = deque()




#####


# Y X
directions = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (-1, 0),
    'R': (0, 1)}

def move(pos, direction):
    dx, dy = directions[direction]



s, g = get_possitions(maze)
print(s)
print(g)