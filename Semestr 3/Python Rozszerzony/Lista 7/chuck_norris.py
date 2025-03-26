import aiohttp
import asyncio

URL = 'https://api.chucknorris.io/jokes/random'

# Funkcja asynchroniczna pobierająca żart
async def fetch_joke(url, i):
    print(f'Pobieram {i} zart!')
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False, timeout=5) as response:
                data = await response.json()
                return data.get('value')
        except aiohttp.ClientError as e:
            print(f'Problem z pobraniem danych dla {url}: {e}')
            return None
        except asyncio.TimeoutError:
            print(f'Czas oczekiwania na odpowiedź dla {url} został przekroczony')
            return None

# Funkcja główna zbierająca żarty w asynchroniczny sposób
async def main():
    try:
        print('Witaj, w generatorze zartow o Chucku Norrisie!')
        num_jokes = int(input("Podaj liczbę żartów do pobrania: "))
        tasks = [fetch_joke(URL, i + 1) for i in range(num_jokes)]
        jokes = await asyncio.gather(*tasks)

        # Wyświetlenie żartów
        for i, joke in enumerate(jokes):
            if joke:
                print(f"Żart {i + 1}: {joke}")
            else:
                print(f"Żart {i + 1}: nie udało się pobrać")

    except ValueError:
        print("Podana wartość nie jest liczbą całkowitą!")

# Uruchomienie programu
if __name__ == "__main__":
    asyncio.run(main())
