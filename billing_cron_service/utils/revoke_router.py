import asyncio
import logging
from contextlib import contextmanager

import backoff
import psycopg2
import requests
from psycopg2.extras import DictCursor

from backoff import log
from settings import settings, pgdb

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "access_token": "",
    "refresh_token": ""
}
site_url = settings.auth_url
sql_select = f"""
        SELECT user_id FROM subscription s 
        WHERE s.end_date < NOW() AND s.is_active = TRUE;
    """


@log
@backoff.on_exception(
    backoff.expo,
    exception=psycopg2.OperationalError,
    max_tries=6
)
def pg_conn(*args, **kwargs):
    return psycopg2.connect(*args, **kwargs)


@contextmanager
def pg_conn_context(*args, **kwargs):
    connection = pg_conn(*args, **kwargs)
    yield connection
    connection.close()


async def update_subscription_table(user_list):
    if len(user_list) == 1:
        where = f"WHERE user_id = '{user_list[0]}'"
    else:
        where = f'WHERE user_id in {tuple(user_list)}'

    sql_update = f"""
            UPDATE subscription
            SET is_active = FALSE
            {where};
        """

    logging.info("We have some user/s in list query will be" + sql_update)

    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql_update)
        pg_connect.commit()

    return logging.info(f"Success_update of {len(user_list)} users")


async def get_subscription_users():
    result_list = []
    with pg_conn_context(**dict(pgdb), cursor_factory=DictCursor) as pg_connect:
        cur = pg_connect.cursor()
        cur.execute(sql_select)
        users = cur.fetchall()

    for user in users:
        result_list.append(user[0])
    logging.info(f"result_list: {result_list}")

    return result_list


async def revoke_subscription_roles():
    # авторизация администратора
    api_url = "v1/auth/login"
    body = {
        "user": "cinema_admin",
        "password": "password"
    }
    url_params = {
        "url": site_url + api_url,
        "json": body,
        "headers": headers
    }
    result = requests.post(**url_params)
    if result.headers.get("access_token") is not None and result.headers.get("refresh_token") is not None:
        headers["access_token"] = result.headers.get("access_token")
        headers["refresh_token"] = result.headers.get("refresh_token")

    if result.status_code == 200:

        # Получение списка пользователей с истекшим сроком подписки
        user_list = await get_subscription_users()

        if user_list:

            # Удаление ролей у пользователей с помощью администратора
            api_url = "/v1/admin/revoke_role_by_id"
            url_params = {
                "url": site_url + api_url,
                "headers": headers
            }
            count = 0
            for user_id in user_list:
                url_params["json"] = {
                    "role_name": "subscriber",
                    "user_id": user_id
                }
                result = requests.post(**url_params)
                if result.status_code == 200:
                    count += 1
            logging.info(f"Success {count} requests. Start updating table")

            # Обновление таблицы подписок
            await update_subscription_table(user_list)
            logging.info("Revoke router sleep for 5 minutes...")
        else:
            logging.warning("No users. Revoke router sleep for 5 minutes...")
    else:
        logging.warning(f"Status code: {result.status_code}. Revoke router sleep for 5 minutes...")

if __name__ == "__main__":
    logging.info("Revoke router started...")
    asyncio.run(revoke_subscription_roles())
