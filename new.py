import asyncio
import requests


async def main(coin1, coin2):
    loop = asyncio.get_event_loop()

    pair = f"{coin1}{coin2}"

    base_url = "https://fapi.binance.com"
    end_point = f"/fapi/v1/klines?interval=1h&symbol={pair}"
    end_point2 = f"/fapi/v1/ticker/price?symbol={pair}"


    while True:
        future1 = loop.run_in_executor(None, requests.get, f"{base_url}{end_point}")
        future2 = loop.run_in_executor(None, requests.get, f"{base_url}{end_point2}")

        response = await future1
        response2 = await future2

        if response.status_code == 200 and response2.status_code == 200:
            resp = response.json()
            resp2 = response2.json()
            current_price = float(resp2['price'])

            prices = []
            for el in resp:
                prices.append(float(el[1]))

            max_price_last_hour = max(prices)
            if max_price_last_hour * 0.99 >= current_price:
                print(f"Current price ({current_price}) is more than 1% less than last hour maximum ({max_price_last_hour})")


if __name__ == '__main__':
    coin1 = 'XRP'
    coin2 = 'USDT'

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main(coin1, coin2))
