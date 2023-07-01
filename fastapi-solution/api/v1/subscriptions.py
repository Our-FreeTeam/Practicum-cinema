import uuid

from core.config import settings
from yookassa import Configuration, Payment

Configuration.account_id = settings.kassa_account_id
Configuration.secret_key = settings.kassa_secret_key