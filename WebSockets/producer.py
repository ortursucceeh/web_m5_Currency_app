import asyncio
import websockets
import sys
from functions import *


async def producer(message: str, host: str, port: int):
    async with websockets.connect(f"ws://{host}:{port}") as ws:
        await write_in_file(message[1:])
        # with inputed currencies 
        if len(message) >= 4 and message[1] == 'exchange' and message[2].isdigit():
            days = int(message[2])
            currencies = [currency.upper().strip() for currency in message[3:]]
            dates = create_dates(days)

            message = await get_exchange(dates=dates, currencies=currencies)

        elif len(message) == 3 and message[1] == 'exchange' and message[2]:
            dates = create_dates(int(message[2]))
            message = await get_exchange(dates=dates)
            
        await ws.send(format_data(message))


if __name__ == '__main__':
    asyncio.run(producer(message=sys.argv, host='localhost', port=4000))