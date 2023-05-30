from abc import abstractmethod, ABC

from dotenv import load_dotenv

load_dotenv()


class AsyncDataStorage(ABC):
    @abstractmethod
    async def get_by_id(self, **kwargs):
        pass

    @abstractmethod
    async def get_list(self, **kwargs):
        pass


class ElasticService(AsyncDataStorage):

    def __init__(self, elastic):
        self.elastic = elastic
