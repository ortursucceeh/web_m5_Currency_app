from datetime import datetime, timedelta

def create_dates():
    days = int(input('Enter count of days(max 10): ')) 
    if days > 10:
        days = days - days % 10
    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime('%d.%m.%Y') for i in range(days)]

data = {
    "date": "22.12.2022",
    "bank": "PB",
    "baseCurrency": 980,
    "baseCurrencyLit": "UAH",
    "exchangeRate": 
      [
        {
            "baseCurrency": "UAH",
            "currency": "EUR",
            "saleRateNB": 24.4808,
            "purchaseRateNB": 24.4808
        },
        {
            "baseCurrency": "UAH",
            "currency": "AZN",
            "saleRateNB": 21.5515,
            "purchaseRateNB": 21.5515
        },
        {
            "baseCurrency": "UAH",
            "currency": "USD",
            "saleRateNB": 21.5515,
            "purchaseRateNB": 21.5515
        }
      ]
}


def get_json_data(data: dict):
    list(filter(lambda x: x["currency"] in ('USD', 'EUR'), data['exchangeRate']))
    currencies = sorted([d for d in data['exchangeRate'] if d["currency"] in ('USD', 'EUR')], key=lambda x: x['currency'])
    eur_info = {'sale': round(currencies[0]['saleRateNB'], 2), 'purchase': round(currencies[0]['purchaseRateNB'], 2)}
    usd_info = {'sale': round(currencies[1]['saleRateNB'], 2), 'purchase': round(currencies[1]['purchaseRateNB'], 2)}
    return {data['date']: {'EUR': eur_info, 'USD': usd_info}}

    
    



print(get_json_data(data))