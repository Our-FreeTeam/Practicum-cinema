import motor.motor_asyncio
from settings import settings

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_url)
database = mongo_client.cinema
