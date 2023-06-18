import time
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from settings import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_mongodb(host=settings.mongodb_host, port=int(settings.mongodb_port), timeout=600):
    client = MongoClient(host=host, port=port)
    start_time = time.time()

    while True:
        try:
            # The 'admin' database is default and should exist in any MongoDB instance.
            client.admin.command('ping')
            logger.info("MongoDB is available! Exiting...")
            break
        except ConnectionFailure:
            if time.time() - start_time > timeout:
                logger.error(f"Cannot connect to MongoDB after {timeout}s. Exiting...")
                break

            logger.info("Cannot connect to MongoDB... Waiting...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_mongodb()
