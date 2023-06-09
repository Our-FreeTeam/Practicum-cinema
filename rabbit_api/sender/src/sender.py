from psycopg2.extras import DictCursor

from config.settings import postgres_settings, email_server_settings, rabbit_settings
from database.connections import create_pg_conn
from utils.email_sender import EmailSender
from models.models import EmailTemplate
from utils.postgres_service import NotificationPostgresService
from utils.worker import Worker

if __name__ == "__main__":
    with create_pg_conn(**postgres_settings.dict(), cursor_factory=DictCursor) as pg_conn:
        # Подключаемся к БД
        postgres_service = NotificationPostgresService(connection=pg_conn, tablename="notifications")
        # Инициализируем сервис отправки писем
        email_sender = EmailSender(email_server_settings, postgres_service)
        # Подключаемся к очереди в Rabbit и принимаем сообщения из очереди
        Worker(rabbit_settings, email_sender, EmailTemplate)
