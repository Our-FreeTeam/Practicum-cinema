import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from api.v1 import subscriptions, statistics
from core.config import settings


description = """
Billing API для приема и возврата платежей за подписку. 🚀

## Subscriptions

Возможность создавать платежи для попдписки, оплачивать их или отменять уже оплаченные
* **Add step 1**
* **cancel**


## Statistics

Возможность просматривать статистику по платежам и подпискам.
Имеется фильтрация по каждому из переменных таблиц с сортировкой по дате подписки/оплаты
Для удобства чтения применена пагинация
"""

tags_metadata = [
    {
        "name": "add",
        "description": "Формирование платежа и отправление данных в ЮKassa",
    },
    {
        "name": "cancel",
        "description": "Отмена платежа",
    },
    {
        "name": "subscription_statistic",
        "description": "Статистика по подпискам",
    },
    {
        "name": "payment_statistic",
        "description": "Статистика по платежам",
    },
]

app = FastAPI(
    title="API для приема и возврата платежей за подписку",
    description=description,
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    contact={
        "name": "Team № 14",
        "url": "https://github.com/Our-FreeTeam/Practicum-cinema"
    },
    default_response_class=ORJSONResponse,
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)


app.include_router(subscriptions.router, prefix='/api/v1/subscriptions', tags=['subscriptions'])
app.include_router(statistics.router, prefix='/api/v1/statistics', tags=['statistics'])
add_pagination(app)


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8200,
    )
