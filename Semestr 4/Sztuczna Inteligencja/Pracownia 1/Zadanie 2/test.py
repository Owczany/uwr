def load_words(filename):
    """Wczytuje zbiór poprawnych słów z pliku."""
    with open(filename, "r", encoding="utf-8") as file:
        return set(word.strip() for word in file)


def reconstruct_text(text, word_set):
    """Odtwarza tekst bez spacji, wstawiając spacje w optymalnych miejscach."""
    longest = max_len(word_set)
    n = len(text)
    dp = [-float("inf")] * (n + 1)
    dp[0] = 0
    split_pos = [-1] * (n + 1)

    for end in range(1, n + 1):
        for start in range(max(0, end - longest), end):  # Ograniczamy długość słów do najdłzuśzego nam znanego słowa
            word = text[start:end]
            if word in word_set:
                score = dp[start] + len(word) ** 2
                if score > dp[end]:
                    dp[end] = score
                    split_pos[end] = start

    if dp[n] == -float("inf"):
        return "NIEMOŻLIWE"

    result = []
    index = n
    while index > 0:
        start = split_pos[index]
        result.append(text[start:index])
        index = start

    return " ".join(reversed(result)) + '\n'


def max_len(dictionary):
    """szybkie sprawdzenie jakie mamy najdłuższe słowo"""
    maximum = 0
    for word in dictionary:
        if len(word) > maximum:
            maximum = len(word)
    return maximum


def process_input_file(input_filename, output_filename, dictionary_filename):
    """Przetwarza plik wejściowy i zapisuje wynik do pliku wyjściowego."""
    word_set = load_words(dictionary_filename)
    # print_max_len(word_set)

    with open(input_filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f]

    results = [reconstruct_text(line, word_set) for line in lines]

    with open(output_filename, "w", encoding="utf-8") as f:
        f.write("".join(results))


if __name__ == "__main__":
    process_input_file("zad2_input.txt", "zad2_output.txt", "polish_words.txt")