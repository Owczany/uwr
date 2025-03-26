import random
from collections import Counter

class Card:
    """Reprezentacja karty do gry."""
    
    VALUES = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "jack": 11, "queen": 12, "king": 13, "ace": 14
    }
    
    COLORS = {"club": '♣️', "diamond": '♦️', "heart": '♥️', "spade": '♠️'} 

    def __init__(self, value, color):
        if color not in Card.COLORS or value not in Card.VALUES:
            raise ValueError("Niepoprawna karta!")
        self.value = value
        self.color = color

    def __str__(self):
        return f'{self.value} {self.COLORS[self.color]}'

    def __repr__(self):
        return f"Card('{self.value}', '{self.color}')"

    def __lt__(self, other):
        return Card.VALUES[self.value] < Card.VALUES[other.value]

    def __eq__(self, other):
        return Card.VALUES[self.value] == Card.VALUES[other.value]

def losuj_karty(deck, liczba_kart=5):
    """Losuje rękę gracza z danej talii."""
    return random.sample(deck, liczba_kart)

# Definicja talii Figuranta (tylko figury) i Blotkarza (tylko blotki)
kolory = ['heart', 'diamond', 'club', 'spade']
figurant_wartosci = ['jack', 'queen', 'king', 'ace']
blotkarz_wartosci = ['2', '3', '4', '5', '6', '7', '8', '9', '10']

figurant_talia = [Card(value, color) for color in kolory for value in figurant_wartosci]
blotkarz_talia = [Card(value, color) for color in kolory for value in blotkarz_wartosci]

# Sprawdzenie rąk pokerowych
def czy_strit(hand):
    """Sprawdza, czy ręka jest stritem."""
    sorted_hand = sorted(hand, key=lambda card: Card.VALUES[card.value])
    return all(Card.VALUES[sorted_hand[i + 1].value] - Card.VALUES[sorted_hand[i].value] == 1 for i in range(len(hand) - 1))

def czy_kolor(hand):
    """Sprawdza, czy wszystkie karty są w tym samym kolorze."""
    return all(card.color == hand[0].color for card in hand)

def czy_poker(hand):
    """Sprawdza, czy ręka to poker (strit w jednym kolorze)."""
    return czy_strit(hand) and czy_kolor(hand)

def analiza_ukladu(hand):
    """Ocena siły układu pokerowego."""
    counter = Counter(Card.VALUES[card.value] for card in hand)

    isFourOfTheKind = 4 in counter.values()
    isThreeOfTheKind = 3 in counter.values()
    numberOfPairs = list(counter.values()).count(2)

    if czy_poker(hand):
        return 9  # Poker królewski lub zwykły
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
        return 2  # Jedna para
    else:
        return 1  # Wysoka karta

def porownanie(hand_f, hand_b):
    """Porównuje ręce graczy i zwraca True, jeśli Figurant wygrał."""
    return analiza_ukladu(hand_f) >= analiza_ukladu(hand_b)

def symulacja(figurant_talia, blotkarz_talia, mecze=10000):
    """Przeprowadza symulację gier i oblicza szansę na wygraną Blotkarza."""
    wygrane_figurant = 0
    wygrane_blotkarz = 0
    
    for _ in range(mecze):
        hand_f = losuj_karty(figurant_talia)
        hand_b = losuj_karty(blotkarz_talia)

        if porownanie(hand_f, hand_b):
            wygrane_figurant += 1
        else:
            wygrane_blotkarz += 1

    procent_blotkarz = (wygrane_blotkarz / mecze) * 100
    print(f'🔹 Figurant wygrał: {wygrane_figurant}, Blotkarz wygrał: {wygrane_blotkarz} (Szansa Blotkarza: {procent_blotkarz:.2f}%)')
    return procent_blotkarz

# Scenariusz 1: Standardowa talia Blotkarza
print("\n🔹 Standardowa talia Blotkarza:")
symulacja(figurant_talia, blotkarz_talia)

# Scenariusz 2: Blotkarz wyrzuca pewne karty
def testuj_rozne_talie_blotkarza():
    """Testuje różne układy talii Blotkarza i wybiera optymalną."""
    najlepsza_talia = None
    najlepsza_skutecznosc = 0

    for i in range(1, len(blotkarz_wartosci)):
        sub_deck_values = blotkarz_wartosci[i - 1:]  # Stopniowe usuwanie słabszych kart
        testowa_talia = [Card(value, color) for color in kolory for value in sub_deck_values]

        print(f"📌 Testujemy talię Blotkarza: {sub_deck_values}")
        wygrane_blotkarz = symulacja(figurant_talia, testowa_talia)

        if wygrane_blotkarz > najlepsza_skutecznosc:
            najlepsza_skutecznosc = wygrane_blotkarz
            najlepsza_talia = sub_deck_values

    print("\n✅ Najlepsza talia Blotkarza:", najlepsza_talia)
    print("🟢 Szansa na wygraną:", round(najlepsza_skutecznosc, 2), "%")

# Scenariusz 3: Blotkarz optymalizuje swoją talię
print("\n🔍 Optymalizacja talii Blotkarza:")
testuj_rozne_talie_blotkarza()

zaproponowana_talia = [Card('10', 'heart'), Card('9', 'heart'), Card('8', 'heart'), Card('7', 'heart'), Card('10', 'spade'), Card('9', 'spade'), Card('10', 'club'), Card('9', 'club'), Card('10', 'diamond'), Card('9', 'diamond')]

symulacja(figurant_talia, zaproponowana_talia)
