import platform
import aiohttp
import asyncio
import json
from pprint import pprint
from datetime import datetime, timedelta

def create_dates() -> list[str]:
    days: int = int(input('Enter count of days(max 10): ')) 
    if days > 10:
        days = days - days % 10
    today: datetime = datetime.today()
    dates: list[str] = [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]
    return dates


def get_json_data(data: dict) -> dict:
    currencies: list = sorted([d for d in data['exchangeRate'] if d["currency"] in ('USD', 'EUR')], key=lambda x: x['currency'])
    eur_info: dict = {'sale': round(currencies[0]['saleRate'], 2), 'purchase': round(currencies[0]['purchaseRate'], 2)}
    usd_info: dict = {'sale': round(currencies[1]['saleRate'], 2), 'purchase': round(currencies[1]['purchaseRate'], 2)}
    return {data['date']: {'EUR': eur_info, 'USD': usd_info}}


def write_in_json(data: dict) -> None:
    
    json_data: list = json.load(open('file.json'))
    json_data.append(data)

    with open('file.json', 'w') as file:
        json.dump(json_data, file, indent=2)


async def get_rate_by_date(session, url):
    print(f'Getting currency rate for {url[-10:]}...')
    async with session.get(url) as response:
        print(f"Status for {url[-10:]}:", response.status)
        all_currencies = await response.json()
        correct_data = get_json_data(all_currencies)
        write_in_json(correct_data)
        return correct_data

async def main():
    async with aiohttp.ClientSession() as session:
        urls = [f'https://api.privatbank.ua/p24api/exchange_rates?date={date}' for date in create_dates()]
        tasks = [asyncio.create_task(get_rate_by_date(session, url)) for url in urls]
        responses = await asyncio.gather(*tasks)
        pprint(responses)




if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
