import aiohttp, asyncio, aiofiles
from aiopath import AsyncPath
from datetime import datetime, timedelta

def create_dates(days: int) -> list[str]:
    if days > 10:
        days = days - days % 10

    today: datetime = datetime.today()    
    return [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]

def get_currencies():
    currencies = input('Enter currencies (separated by space): ').split()
    return  [currency.upper().strip() for currency in currencies]


def get_currencies_data(data: dict, searched_currencies: list[str]) -> dict:
    currencies_data: list = [d for d in data['exchangeRate'] if d["currency"] in searched_currencies]
    all_currencies_info: dict = {}

    for currency, currency_data in zip(searched_currencies, currencies_data):
        currency_exchange_info: dict = {'sale': round(currency_data['saleRate'], 2), 'purchase': round(currency_data['purchaseRate'], 2)}
        all_currencies_info.update({currency: currency_exchange_info})

    return {data['date']: all_currencies_info}


async def write_in_file(data: list) -> None:
    date_time = datetime.now().strftime('%d.%m.%Y - %H:%M:%S')
    path = AsyncPath('logging.txt')
    regym = 'a' if await path.exists() else 'w'
    async with aiofiles.open('logging.txt', regym) as file:
        await file.write(f'{date_time} --- {data}\n')
 






async def get_rate_by_date(session, url, currencies):
    async with session.get(url) as response:

        all_currencies = await response.json()
        correct_data = get_currencies_data(all_currencies, currencies)

        return correct_data


async def get_exchange(dates, currencies=('USD', 'EUR')):
    async with aiohttp.ClientSession() as session:
        urls = [f'https://api.privatbank.ua/p24api/exchange_rates?date={date}' for date in dates]
        tasks = [asyncio.create_task(get_rate_by_date(session, url, currencies)) for url in urls]
        responses = await asyncio.gather(*tasks)
        return responses

def format_data(data: list[dict]):
    result = '\n'
    for dictionary in data:
        for date, value in dictionary.items():
            result += f'{date}\n'
            for currency, cur_data in value.items():
                result += f"{currency}\n\t{cur_data}\n"
    return result

    