from private_keys import API_KEY
import aiohttp
import asyncio
import json

async def fetch_data(lat, long, city):
    async with aiohttp.ClientSession() as session:
        try:    
            async with session.get(f'https://api.waqi.info/feed/geo:{lat};{long}/?token={API_KEY}', ssl=False, timeout=5) as response:
                data = await response.json()
                # print(json.dumps(data, indent=4))
                return f'{city}: {str(data['data']['aqi'])}'
                
        except aiohttp.ClientError as e:
            print(f'Problem z pobraniem danych dla koordynatów [{lat}, {long}]')
            return city

        except asyncio.TimeoutError:
            print(f'Czas oczekiwania na odpowiedź dla  koordynatów [{lat}, {long}]został przekroczony')
            return city


locations = {
    'Warsaw': (52.235026, 21.01642),
    'Wroclaw': (51.122982, 17.012088),
    'Paris': (48.852952, 2.347719),
    'London': (51.467943, -0.134796),
    'Venezia': (45.483433, 12.286384),
    'Unknown': (29.491578, -41.348091)
}

async def main():

    print('Witaj, w systemie sprawdzającym jakoś powietrza!')
    tasks = [fetch_data(locations[city][0], locations[city][1], city) for city in locations]
    airs = await asyncio.gather(*tasks)

    # Wyświetlenie żartów
    for i, air in enumerate(airs):
        if air:
            print(f"{air}")
        else:
            print(f"Nie udało się pobrać dannych dla {air}")


# Uruchomienie programu
if __name__ == "__main__":
    asyncio.run(main())
