import itertools
from collections import Counter

class Card:
    """Reprezentacja karty do gry."""
    
    VALUES = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
        "8": 8, "9": 9, "10": 10,
        "jack": 11, "queen": 12, "king": 13, "ace": 14
    }
    
    COLORS = {"club": '♣️', "diamond": '♦️', "heart": '♥️', "spade": '♠️'} 

    def __init__(self, value, color):
        if color not in Card.COLORS or value not in Card.VALUES:
            raise ValueError("Niepoprawna karta!")
        self.value = value
        self.color = color

    def __repr__(self):
        return f"Card('{self.value}', '{self.color}')"

    def __lt__(self, other):
        return Card.VALUES[self.value] < Card.VALUES[other.value]

    def __eq__(self, other):
        return Card.VALUES[self.value] == Card.VALUES[other.value]

# Talia Figuranta (tylko figury) i Blotkarza (tylko blotki)
kolory = ['heart', 'diamond', 'club', 'spade']
figurant_wartosci = ['jack', 'queen', 'king', 'ace']
blotkarz_wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10']

figurant_talia = [Card(value, color) for color in kolory for value in figurant_wartosci]
blotkarz_talia = [Card(value, color) for color in kolory for value in blotkarz_wartosci]

# --- Funkcje do analizy układów ---

def czy_strit(hand):
    """Sprawdza, czy ręka jest stritem."""
    sorted_hand = sorted(hand, key=lambda card: Card.VALUES[card.value])
    return all(
        Card.VALUES[sorted_hand[i + 1].value] - Card.VALUES[sorted_hand[i].value] == 1
        for i in range(len(hand) - 1)
    )

def czy_kolor(hand):
    """Sprawdza, czy wszystkie karty są w tym samym kolorze."""
    return all(card.color == hand[0].color for card in hand)

def czy_poker(hand):
    """Sprawdza, czy ręka to poker (strit w jednym kolorze)."""
    return czy_strit(hand) and czy_kolor(hand)

def analiza_ukladu(hand):
    """
    Zwraca ocenę układu w skali 1..9, gdzie wyższa liczba oznacza silniejszy układ.
    Uwaga: nie rozróżniamy w obrębie rangi np. "para króli" od "pary dwójek" – 
    mamy jedynie klasę "para" itp.
    """
    counter = Counter(Card.VALUES[card.value] for card in hand)
    isFourOfTheKind = 4 in counter.values()
    isThreeOfTheKind = 3 in counter.values()
    numberOfPairs   = list(counter.values()).count(2)

    if czy_poker(hand):
        return 9  # Poker
    elif isFourOfTheKind:
        return 8  # Kareta
    elif isThreeOfTheKind and numberOfPairs == 1:
        return 7  # Full
    elif czy_kolor(hand):
        return 6  # Kolor
    elif czy_strit(hand):
        return 5  # Strit
    elif isThreeOfTheKind:
        return 4  # Trójka
    elif numberOfPairs == 2:
        return 3  # Dwie pary
    elif numberOfPairs == 1:
        return 2  # Para
    else:
        return 1  # Wysoka karta

# --- Główna funkcja enumerująca wszystkie możliwe układy ---

def oblicz_dokladne_prawdopodobienstwo_blotkarza(figurant_deck, blotkarz_deck):
    """
    Oblicza (dokładnie, bez symulacji) prawdopodobieństwo wygranej Blotkarza
    w starciu z Figurantem, zakładając regułę:
      - Figurant wygrywa, jeśli rank_f >= rank_b,
      - Blotkarz wygrywa, jeśli rank_f < rank_b.
    """

    # 1) Policz liczbę wystąpień poszczególnych rang układu (1..9) dla Figuranta.
    rank_count_fig = [0]*10  # Indeksy od 0 do 9, nie będziemy używać 0
    for combo_f in itertools.combinations(figurant_deck, 5):
        rf = analiza_ukladu(combo_f)
        rank_count_fig[rf] += 1

    # 2) Policz liczbę wystąpień poszczególnych rang układu (1..9) dla Blotkarza.
    rank_count_bl = [0]*10
    for combo_b in itertools.combinations(blotkarz_deck, 5):
        rb = analiza_ukladu(combo_b)
        rank_count_bl[rb] += 1

    # 3) Oblicz całkowitą liczbę par (figurantowa ręka, blotkarzowa ręka).
    #    Jest to binom(16,5) * binom(36,5) dla pełnych talii, ale my policzymy wprost.
    total_pairs = sum(rank_count_fig) * sum(rank_count_bl)

    # 4) Oblicz liczbę par, w których Blotkarz wygrywa (czyli rank_f < rank_b).
    #    Z drugiej strony, pary w których rank_f >= rank_b należą do Figuranta.
    blotkarz_wins = 0

    for rf in range(1, 10):        # wszystkie możliwe rangi figuranta
        for rb in range(1, 10):    # wszystkie możliwe rangi blotkarza
            count_pairs = rank_count_fig[rf] * rank_count_bl[rb]
            if rf < rb:  
                blotkarz_wins += count_pairs

    # 5) Prawdopodobieństwo wygranej Blotkarza:
    p_blotkarz = blotkarz_wins / total_pairs
    return p_blotkarz

# --- Wywołanie i prezentacja wyniku ---

if __name__ == "__main__":
    p_blotkarz = oblicz_dokladne_prawdopodobienstwo_blotkarza(figurant_talia, blotkarz_talia)
    print(f"Dokładne P(Blotkarz wygrywa) = {p_blotkarz:.6f}  (czyli ok. {100 * p_blotkarz:.2f}%)")
