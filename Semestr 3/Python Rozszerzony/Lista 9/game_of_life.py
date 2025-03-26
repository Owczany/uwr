from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random

HEIGHT = random.randrange(10, 51)
WIDTH = random.randrange(HEIGHT, HEIGHT + 41)
print(HEIGHT)
print(WIDTH)

# Żywa komórka - 1, martwa - 0
# Przykładowa plansza
matrix = np.array([
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 1, 0, 0, 1]
])

matrix2 = np.array([
    [1, 1],
    [1, 0]
])

random_matrix = np.random.randint(0, 2, size=(HEIGHT, WIDTH))

print(random_matrix)

# Przypisanie jakieś planszy do naszej
board = random_matrix

def isFinished():
    rows, cols = board.shape
    next_board = next_generation(board)


    for row in range(rows):
        for col in range(cols):
            if board[row, col] != next_board[row, col]:
                return False

    return True

def frame_generator(matrix):
    frame = 1
    while not isFinished():
        yield frame
        frame += 1

def next_generation(board):
    # Tworzenie kopii planszy dla nowej generacji
    next_board = board.copy()
    rows, cols = board.shape

    for row in range(rows):
        for col in range(cols):
            neighbours = 0

            # Współrzędne sąsiadów
            coords = [
                (row, col + 1),
                (row + 1, col + 1),
                (row + 1, col),
                (row + 1, col - 1),
                (row, col - 1),
                (row - 1, col - 1),
                (row - 1, col),
                (row - 1, col + 1)
            ]
            
            # Liczenie sąsiadów
            for y, x in coords:
                if 0 <= y < rows and 0 <= x < cols and board[y, x]:  # Upewnienie się, że nie wychodzimy poza granice
                    neighbours += 1

            # Reguły gry w życie:
            if board[row, col]:  # Komórka żywa
                if neighbours < 2 or neighbours > 3:  # Umiera z niedo-/przeludnienia
                    next_board[row, col] = 0
            else:  # Komórka martwa
                if neighbours == 3:  # Ożywa przez reprodukcję
                    next_board[row, col] = 1

    return next_board


# Tworzenie mapy kolorów
cmap = ListedColormap(["white", "black"])  # 0 → biały, 1 → czarny

# Tworzenie figury i osi
fig, ax = plt.subplots()

# Wyświetlenie obrazu
img = ax.imshow(board, cmap=cmap)

# Początek wyswietlania
def init():
    ax.set_title('The Game of Life')
    img.set_data(board)
    return [img]


def update(frame):
    global board
    board = next_generation(board)  # Aktualizacja planszy
    img.set_data(board)  # Aktualizacja danych w obrazie
    ax.set_title(f'Generacja {frame}')  # Aktualizacja tytułu
    return [img]

# Dodanie siatki
ax.set_xticks(np.arange(-0.5, board.shape[1], 1), minor=True)  # Pozycje poziomej siatki
ax.set_yticks(np.arange(-0.5, board.shape[0], 1), minor=True)  # Pozycje pionowej siatki
ax.grid(which="minor", color="gray", linestyle="-", linewidth=0.5)  # Siatka nad obrazem

# Wyłączenie głównych etykiet osi
ax.tick_params(which="minor", bottom=False, left=False)
ax.set_xticks([])
ax.set_yticks([])

frames = frame_generator(matrix)

# Tworzenie animacji
ani = FuncAnimation(
    fig, update, init_func=init, frames=frames, interval=50, blit=False, repeat=False
)

# Wyświetlanie animacji
plt.show()
