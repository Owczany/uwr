from collections import deque

INPUT_FILE = 'zad2_input.txt'
OUTPUT_FILE = 'zad2_output.txt'

# Przykładowe labirytnty
maze = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],

    ]

simple_maaze = [['#', '#', '#', '#', '#'],
                ['#', ' ', ' ', ' ', '#'],
                ],

#Komentarz

def read_input_file(filename):
    def get(line):

        return [x for x in line]

    with open(filename, 'r') as f:
        return [get(char) for char in [line for line in f.readline()]]

print(read_input_file(INPUT_FILE))