import aiohttp
import asyncio
import statistics
from matplotlib import pyplot as plt

# Parametry
params = {'format': 'json'}

# Lista miesięcy
months = [
    'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 
    'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
]

# Funkcja zwracająca listę wartości waluty w danym roku
async def get_currency_values(session, code, year):
    values = []
    months_numeric = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    for i in range(len(months_numeric)):
        if i < len(months_numeric) - 1:
            next_year = year
            next_month = months_numeric[i + 1]
        else:
            next_year = str(int(year) + 1)
            next_month = '01'

        url = f'https://api.nbp.pl/api/exchangerates/rates/A/{code}/{year}-{months_numeric[i]}-01/{next_year}-{next_month}-01'

        try:
            async with session.get(url, ssl=False, timeout=5, params=params) as response:
                data = await response.json()
                rates = [float(rate['mid']) for rate in data['rates']]
                values.append(round(statistics.mean(rates), 5))

        except aiohttp.ClientError as e:
            print(f'Problem z pobraniem danych dla {url}: {e}')
            return None

        except asyncio.TimeoutError:
            print(f'Czas oczekiwania na odpowiedź dla {url} został przekroczony')
            return None

        except Exception as e:
            print(f'Wystąpił nieznany błąd: {e}')
            return None

    return values

def predict(data):
    res = [0 for _ in range(12)]
    for item in data:
        for i in range(len(item)):
            res[i] += item[i]
    
    for i in range(len(res)):
        res[i] = res[i] / len(data)

    return res


# Funkcja główna
async def main():
    async with aiohttp.ClientSession() as session:

        # Pobieranie danych równolegle
        usd_2021, eur_2021, usd_2022, eur_2022 = await asyncio.gather(*[
            get_currency_values(session, 'usd', '2021'),
            get_currency_values(session, 'eur', '2021'),
            get_currency_values(session, 'usd', '2022'),
            get_currency_values(session, 'eur', '2022')
        ])

        predict_usd = predict([usd_2021, usd_2022])
        predict_eur = predict([eur_2021, eur_2022])

        # Tworzenie wykresu
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

        # Wykres dla 2021
        if usd_2021 and eur_2021:
            ax1.plot(months, usd_2021, color='red', label='Dolar Amerykański')
            ax1.plot(months, eur_2021, color='green', label='Euro')
            ax1.legend()
            ax1.set_title('Średnie miesięczne wartości walut w 2021 roku')
            ax1.set_xlabel('Miesiąc')
            ax1.set_ylabel('Wartość w PLN')

        # Wykres dla 2022
        if usd_2022 and eur_2022:
            ax2.plot(months, usd_2022, color='red', label='Dolar Amerykański')
            ax2.plot(months, eur_2022, color='green', label='Euro')
            ax2.legend()
            ax2.set_title('Średnie miesięczne wartości walut w 2022 roku')
            ax2.set_xlabel('Miesiąc')
            ax2.set_ylabel('Wartość w PLN')

        if predict_usd and predict_eur:
            ax3.plot(months, predict_usd, color='red', label='Dolar Amerykański')
            ax3.plot(months, predict_eur, color='green', label='Euro')
            ax3.legend()
            ax3.set_title('Przewidywane średnie miesięczne wartości walut w 2023 roku')
            ax3.set_xlabel('Miesiąc')
            ax3.set_ylabel('Wartość w PLN')

        # Wyświetlanie wykresów
        plt.tight_layout()
        plt.show()


# Uruchomienie programu
if __name__ == "__main__":
    asyncio.run(main())
