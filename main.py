import asyncio

from websockets.server import serve

from settings import settings
from ws import handle_client


async def main():
    async with serve(handle_client, settings.APP_HOST, settings.APP_PORT):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
