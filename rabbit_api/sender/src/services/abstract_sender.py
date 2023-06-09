from abc import ABC, abstractmethod

from services.abstract_database_service import AbstractNotificationDatabaseService


class AbstractSender(ABC):
    """Абстрактная реализация объекта, который занимается отправкой сообщений, вне зависимости от типа сообщений"""
    @abstractmethod
    def __init__(self, database: AbstractNotificationDatabaseService):
        self.database = database

    @abstractmethod
    def send(self, data):
        """В классе-наследнике обязательно должен быть реализован метод отправки сообщений"""
        pass
