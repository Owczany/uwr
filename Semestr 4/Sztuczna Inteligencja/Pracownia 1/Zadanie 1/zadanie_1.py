import argparse
from collections import deque

# Plik wejściowy i wyjściowy
INPUT_FILE = 'zad1_input.txt'
OUTPUT_FILE = 'zad1_output.txt'

def read_input_file(filename):
    """Wczytuje dane wejściowe."""
    with open(filename, 'r') as f:
        return [line.strip().split() for line in f.readlines()]

def write_output_file(filename, results):
    """Zapisuje wyniki do pliku."""
    with open(filename, 'w') as f:
        for result in results:
            f.write(str(result) + "\n")

# Konwersja notacji szachowej np. 'a1' -> (0, 0)
def convert_position(pos):
    converter = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    return (converter[pos[0]], int(pos[1]) - 1)

def convert_chess(pos):
    return chr(pos[0] + ord('a')) + str(pos[1] + 1)

def valid_rook_moves(white_rook_position, white_king_position, black_king_position):
    """Zwraca możliwe ruchy wieży."""
    col, row = white_rook_position
    valid_positions = set()

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        while 0 <= new_col <= 7 and 0 <= new_row <= 7:
            # Biała wieża nie może przejść przez swojego króla
            if (new_col, new_row) == white_king_position:
                break

            valid_positions.add((new_col, new_row))
            new_col, new_row = new_col + dc, new_row + dr

    return valid_positions

# Kandydaci na ruch króla
def possible_king_moves(king_position):
    """Zwraca wszystkie możliwe ruchy króla."""
    possible_positions = set()
    col, row = king_position
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    
    for dc, dr in directions:
        new_col, new_row = col + dc, row + dr
        if 0 <= new_col <= 7 and 0 <= new_row <= 7:
            possible_positions.add((new_col, new_row))

    return possible_positions

def valid_white_king_moves(white_king_position, white_rook_position, black_king_position):
    """Zwraca poprawne ruchy białego króla."""
    return possible_king_moves(white_king_position).difference(
        possible_king_moves(black_king_position).union({white_rook_position})
    )

def valid_black_king_moves(black_king_position, white_rook_position, white_king_position):
    """Zwraca poprawne ruchy czarnego króla."""
    return possible_king_moves(black_king_position).difference(
        valid_rook_moves(white_rook_position, white_king_position, black_king_position).union(
            possible_king_moves(white_king_position).union({white_rook_position})
        )
    )

def solve(color_to_move, white_king_position, white_rook_position, black_king_position):
    """Rozwiązuje problem szachowy przy pomocy BFS."""
    visited = set()
    queue = deque([(color_to_move, white_king_position, white_rook_position, black_king_position, [])])

    while queue:
        color_to_move, white_king_position, white_rook_position, black_king_position, moves = queue.popleft()

        if (color_to_move, white_king_position, white_rook_position, black_king_position) in visited:
            continue
        
        visited.add((color_to_move, white_king_position, white_rook_position, black_king_position))

        if len(valid_black_king_moves(black_king_position, white_rook_position, white_king_position)) == 0 \
                and black_king_position in valid_rook_moves(white_rook_position, white_king_position, black_king_position) \
                and white_rook_position not in possible_king_moves(black_king_position):
            return str(len(moves)), moves

        if color_to_move == 'white':
            for new_white_rook_position in valid_rook_moves(white_rook_position, white_king_position, black_king_position):
                queue.append(('black', white_king_position, new_white_rook_position, black_king_position, moves + [(white_king_position, new_white_rook_position, black_king_position)]))
            for new_white_king_position in valid_white_king_moves(white_king_position, white_rook_position, black_king_position):
                queue.append(('black', new_white_king_position, white_rook_position, black_king_position, moves + [(new_white_king_position, white_rook_position, black_king_position)]))
        else:
            for new_black_king_position in valid_black_king_moves(black_king_position, white_rook_position, white_king_position):
                queue.append(('white', white_king_position, white_rook_position, new_black_king_position, moves + [(white_king_position, white_rook_position, new_black_king_position,)]))

    return 'INF', []

def main():
    """Główna funkcja programu."""
    
    # Tworzymy parser argumentów
    parser = argparse.ArgumentParser(description="Program do rozwiązywania końcówek szachowych.")
    
    parser.add_argument("--debug", nargs=4, metavar=("COLOR", "WK_POS", "WR_POS", "BK_POS"),
                        help="Tryb debugowania. Podaj kolejno: kolor ('white' lub 'black'), pozycję białego króla, pozycję wieży, pozycję czarnego króla.")
    
    # Parsujemy argumenty
    args = parser.parse_args()
    
    if args.debug:
        start_color, wk_pos, wr_pos, bk_pos = args.debug
        color_to_move = start_color
        white_king_position = convert_position(wk_pos)
        white_rook_position = convert_position(wr_pos)
        black_king_position = convert_position(bk_pos)
        move_num, match = solve(color_to_move, white_king_position, white_rook_position, black_king_position)
        print("\n🔹 Tryb debugowania")
        print(f"Kolor ruchu: {start_color}")
        print(f"Biały król: {wk_pos}")
        print(f"Biała wieża: {wr_pos}")
        print(f"Czarny król: {bk_pos}")
        
        print("\n🔹 Minimalna liczba ruchów do mata:", move_num)
        print("🔹 Przebieg gry:")
        for move in match:
            wk, wr, bk = move
            print(f"White King: {convert_chess(wk)}, White Rook: {convert_chess(wr)}, Black King: {convert_chess(bk)}")
        
    else:
    
        data = read_input_file(INPUT_FILE)
        results = []

        for line in data:
            start_color, wk_pos, wr_pos, bk_pos = line
            color_to_move = start_color
            white_king_position = convert_position(wk_pos)
            white_rook_position = convert_position(wr_pos)
            black_king_position = convert_position(bk_pos)

            move_num, match = solve(color_to_move, white_king_position, white_rook_position, black_king_position)
            results.append(move_num)
                
        write_output_file(OUTPUT_FILE, results)

# Uruchamianie programu
if __name__ == '__main__':
    main()
