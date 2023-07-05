import asyncio
import logging

from settings import settings


async def main():
    logging.basicConfig(format=settings.log_format, level="INFO")


if __name__ == "__main__":
    asyncio.run(main())
