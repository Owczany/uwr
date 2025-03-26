import requests
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import re
import time

# Przykładowe linki
urls = [
    'https://example.com',
    'https://www.youtube.com',
    'https://skos.ii.uni.wroc.pl',
    'https://pl.khanacademy.org',
    'https://www.netflix.com',
]

class WebIndexer:
    # Konstruktor, który przyjmuje linki do stron
    def __init__(self, urls):
        self.urls = urls # Linki
        self.indexes = defaultdict(Counter) # Indeksy dla danych stron 

    # Funkcja w klasie, która ściąga dane ze strony
    def fetch_page(self, url):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'Problem z pobraniem danych dla {url}: {e}')
            return None
        except:
            print('Napotkano nieznany problem')
            return None

    def parse_words(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        words = re.findall(r'\w+', soup.get_text().lower())
        return words

    # Funkcja, która tworzy indexy dla linków
    def create_indexes(self):
        for url in self.urls:
            print(f'Pobieram dane z [{url}]')
            page_content = self.fetch_page(url)
            if page_content:
                words = self.parse_words(page_content)
                self.indexes[url].update(Counter(words))
                time.sleep(1)

    def most_popular_word(self, url):
        if url in urls:
            most_common_word, frequency = self.indexes[url].most_common(1)[0]
            return most_common_word, frequency
        else:
            print(f'Podano zły link: {url}')
            return None, 0

    def find_word_in_sites(self, word):
        sites = set()
        for url in self.urls:
            if word in self.indexes[url]:
                sites.add(url)
        if sites:
            print(f'Słowo [{word}] występuje na stonach: [{sites}]')
            return sites
        print(f'Słowo [{word}] nie występuje na zadnej z podanych stron!')
        return None
    
# Tworzenie objektu WebIndexer
indexer = WebIndexer(urls)
indexer.create_indexes()

# Sprawdzanie indexu dla example.com
if 'https://example.com' in indexer.indexes:
    print('Wypisuje index dla https://example.com')
    print(indexer.indexes['https://example.com'])
    print('Koniec indexu dla https://example.com')
    print()
else:
    print('Nie sprawdzono indeksu dla podanego linku')

# Sprawdzanie najczęstszych wyrazów
for url in urls:
    most_common_word, frequency = indexer.most_popular_word(url)
    if most_common_word:
        print(f'Na stronie: {url} najczęstszym słowem jest [{most_common_word}] i występuje {frequency} razy!')
print()
# Sprawdzanie czy dane słowo występuje na stronach
indexer.find_word_in_sites('is')
print()
indexer.find_word_in_sites('example')
print()
indexer.find_word_in_sites('niemamnie')
