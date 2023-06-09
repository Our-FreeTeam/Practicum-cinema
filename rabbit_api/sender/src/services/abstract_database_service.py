from abc import ABC, abstractmethod

from models.models import Notification


class AbstractNotificationDatabaseService(ABC):
    """Абстракция объекта, которые реализует сохранение/получение Уведомлений в выбранной БД"""
    @abstractmethod
    def __init__(self, connection):
        self.connection = connection

    @abstractmethod
    def save_notification_to_db(self, notification: Notification):
        """Метод по сохранению Уведомления в БД"""
        pass

    @abstractmethod
    def get_notification_by_id(self, notification_id, user_id):
        """Метод по получению уведомления по заданному ID"""
        pass
