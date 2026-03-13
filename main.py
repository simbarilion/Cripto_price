import asyncio

from app.services.deribit_client import DeribitClient


async def main():
    client = DeribitClient()
    prices = await client.fetch_all_prices()
    print(prices)


if __name__ == "__main__":
    asyncio.run(main())


# from fastapi import FastAPI
#
# app = FastAPI()
#
#
# @app.get("/")
# def root():
#     return {"message": "Crypto API running"}