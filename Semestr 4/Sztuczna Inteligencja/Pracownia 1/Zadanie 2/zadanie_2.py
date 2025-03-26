# Pliki
INPUT_FILE = 'zad2_input.txt'
OUTPUT_FILE = 'zad2_output.txt'
WORDS_FILE = 'polish_words.txt'

def load_words(filename):
    """Wczytuje zbiór poprawnych słów z pliku."""
    with open(filename, "r", encoding="utf-8") as file:
        return set(word.strip() for word in file)
    
def read_input_file(filename):
     with open(filename, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def write_output_file(filename, sentences):
    with open(filename, "w", encoding="utf-8") as file:
        file.writelines(sentences)

def reconstruct_text(text, word_set):
    longest_word = len(find_longest_word(word_set))
    n = len(text)
    scores = [-float('inf')] * (n + 1)
    scores[0] = 0
    space_pos = [-1] * (n + 1)
    
    for end in range(1, n + 1):
        for start in range(max(0, end - longest_word), end):
            word = text[start:end]
            if word in word_set:
                score = scores[start] + len(word) ** 2
                if score > scores[end]:
                    scores[end] = score
                    space_pos[end] = start
                                        
    if scores[n] == -float('inf'):
        return 'NIEMOŻLIWE\n'
    
    chosen_words = []
    index = n
    while index > 0:
        start = space_pos[index]
        chosen_words.append(text[start:index])
        index = start

    return " ".join(reversed(chosen_words)) + '\n'
    
def find_longest_word(words):
    longest_word = ''
    for word in words:
        if len(longest_word) < len(word):
            longest_word = word
    return longest_word
    
def main():
    words = load_words(WORDS_FILE)
    sentences = [reconstruct_text(text, words) for text in read_input_file(INPUT_FILE)]
    write_output_file(OUTPUT_FILE, sentences)
    
if __name__ == '__main__':
    main()