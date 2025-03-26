import aiohttp
import asyncio
from bs4 import BeautifulSoup
from collections import defaultdict, Counter
import re
from asyncio.locks import Lock

# Przykładowe linki
urls = [
    'https://example.com',
    'https://www.youtube.com',
    'https://skos.ii.uni.wroc.pl',
    'https://pl.khanacademy.org',
    'https://www.netflix.com',
]

class AsyncWebIndexer:
    def __init__(self, urls):
        self.urls = urls
        self.indexes = defaultdict(Counter)
        self.lock = Lock()

    async def fetch_page(self, session, url):
        try:
            async with session.get(url, ssl=False, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except aiohttp.ClientError as e:
            print(f'Problem z pobraniem danych dla {url}: {e}')
            return None
        except asyncio.TimeoutError:
            print(f'Czas oczekiwania na odpowiedź dla {url} został przekroczony')
            return None

    def parse_words(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        words = re.findall(r'\w+', soup.get_text().lower())
        return words

    async def create_indexes(self):
        async with aiohttp.ClientSession() as session:
            # for url in self.urls:
            #     await self.index_site(session, url)
            tasks = [self.index_site(session, url) for url in self.urls]
            await asyncio.gather(*tasks)

    async def index_site(self, session, url):
        print(f'Pobieram dane z [{url}]')
        page_content = await self.fetch_page(session, url)
        if page_content:
            words = self.parse_words(page_content)
            async with self.lock:  # Zapewnia bezpieczeństwo operacji na współdzielonej strukturze
                self.indexes[url].update(Counter(words))
            print(f'Indeksowanie zakończone dla {url}')

    def most_popular_word(self, url):
        if url in self.indexes:
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
            print(f'Słowo [{word}] występuje na stronach: [{sites}]')
            return sites
        print(f'Słowo [{word}] nie występuje na żadnej z podanych stron!')
        return None

# Tworzenie obiektu AsyncWebIndexer
indexer = AsyncWebIndexer(urls)

async def main():
    await indexer.create_indexes()

    # Sprawdzanie najczęstszych wyrazów
    for url in urls:
        most_common_word, frequency = indexer.most_popular_word(url)
        if most_common_word:
            print(f'Na stronie: {url} najczęstszym słowem jest [{most_common_word}] i występuje {frequency} razy!')

    print()
    # Sprawdzanie, czy dane słowo występuje na stronach
    indexer.find_word_in_sites('is')
    print()
    indexer.find_word_in_sites('example')
    print()
    indexer.find_word_in_sites('niemamnie')

# Uruchamianie programu
asyncio.run(main())
