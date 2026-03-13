import aiohttp


URL = "https://www.deribit.com/api/v2/public/get_index_price"


async def get_price(ticker: str):

    params = {"index_name": ticker}

    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params) as response:
            data = await response.json()
            return data["result"]["index_price"]
