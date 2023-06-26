# Проектная работа 10 спринта Notification

Задание Notification (RabbitMQ)

1. Сервис mailercron_service-e2q собирает раз в неделю почтовые адреса пользователей из сервиса
   авторизации и отправляет в точку обмена с задержкой отправки равной времени в секундах
   до ближайшей пятницы 15:00 по местному времени получателя (планируем отправить пользователю
   еженедельную рассылку с информацией о том сколько фильмов он посмотрел)

2. Сервис mailercron_service-qe забирает адреса пользователей из очереди (при достижении 
   правильного времени)
   и создает текст письма обращаясь к API ugc (получая оттуда данные по просмотрам фильмов для)
   пользователей и отправляет обратно в новую очередь

3. Сервис sender получает из очереди письма и отправляет их конечным пользователям
   (попытка интегрировать подключение к sendgrid не увенчалась успехом, при попытке обращения
   к API сервиса с правильным ключом возвращается ошибка 404)


Для разворачивания проекта использовать env.example и build_dev.bat,
Либо разворачивать по очереди
docker-compose-logs.yml,
docker-compose-mongo-solo.yml,
docker-compose-authsubsys.yml,
docker-compose-rabbit.yml,
docker-compose-sender.yml,
docker-compose.yml,

Ссылка на репозиторий https://github.com/Our-FreeTeam/Practicum-cinema
Ссылка на Sentry https://our-freeteam.sentry.io/issues/




# Структура проекта
```
├── UML_schema/                         # Папка с архитектурой проекта в UML (спринт 8)
    ├── current/                        
        ├── current_uml_schema_C1.txt   #  текущая - уровень C1
        ├── current_uml_schema_C2.txt   #  текущая - уровень C2
    ├── planned/                        
        ├── next_uml_schema_C1.txt      #  новая - уровень C1
        ├── next_uml_schema_C2.txt      #  новая - уровень C2 
        ├── next_uml_schema_C3.txt      #  новая - уровень C3                


├── flaskapi-solution/              # Основная папка приложения Flask
    ├── views/                        
        ├── v1/                     # Папка с api версии 1
            ├── admin.py            # файл ручек админа
            ├── auth.py      
    ├── models/                  
        ├── models.py               # файл со всеми моделями проекта  
    ├── app.py                      # основной файл запуска проекта
    ├── requirements.txt            # файл с зависимостями для Flask
    ├── Dockerfile                  # Dockerfile контейнера Flask-solution
    ├── keycloack_conn.py           # файл с подключением к keycloak
    ├── messages.py                 # файл с ответами ручек
    ├── settings.py                 # файл с настройками
    ├── utils.py                    # файл с вспомогательными функциями
    ├── create_su.py                # создание суперпользователя для realm cinema
    ├── wait_for_keycloak.py        # Вейтер запуска KeyCloak


├── keycloak/                       # папка KeyCloak
    ├── import                      # 
        ├── realm-export.json       # файл с базовыми настройками сервиса KeyCloak, в т.ч. 
                                    # настройки Realm - Cinema и клиента Theatre с помощью 
                                    # которого будет подключатся Flask к KeyCloak
    ├── providers                   # папка с аддонами для импорта (провайдеры OAuth)
        ├── keycloak-russian-providers-1.0.49.jar  # файл с плагинами для RU сервисов
    ├── Dockerfile                  # Dockerfile контейнера KeyCloak


├── fastapi-solution/               # Основная папка приложения FastAPI
    ├── api/                        
        ├── v1/                     # Папка с api версии 1
            ├── films.py            # поиск по фильмам
            ├── genres.py           # поиск по жанрам
            ├── persons.py          # поиск по персонам
    ├── core/                  
        ├── config.py               # файл настроек проекта
        ├── logger.py               # файл настроек логгера
    ├── db/                         # папка с функциями для работы с redis и elastic
        ├── elastic.py              # elastic
        ├── redis.py                # redis
    ├── models/                     # папка с файлами моделей
        ├── models.py               # файл со всеми моделями проекта   
    ├── services/                   # папка с функциями обработки данных
        ├── common_service.py       # главная библиотека обработки и кеширования данных
        ├── elastic_query_collection.py # коллеция запросов для Elastic
        ├── film.py                 # мостик film api - commons_ervice
        ├── genre.py                # мостик genre api - common_service
        ├── person.py               # мостик person api - common_service
        ├── messages.py             # messages for user if errors in api
    ├── main.py                     # основной файл запуска проекта
    ├── requirements.txt            # файл с зависимостями для FastAPI
    ├── Dockerfile                  # Dockerfile контейнера FastApi-solution
       

├── db/                             # Работа с БД
    ├── models.py                   # Модели SQLAlchemy
    ├── movies_dataclasses.py       # Датаклассы для переливки данных из SQLite в PostgreSQL
    
    
├── etl/                            # Работа с ETL
    ├── sql/                        # папка с данными из БД в формате sql
    ├── alembic.ini                 # Конфигурационный файл alembic
    ├── create_es_schema.sh         # Скрипт создания индексов в ElasticSearch
    ├── data_transform.py           # Модуль преобразования данных перед заливкой в ElasticSearch
    ├── Dockerfile                  # Dockerfile контейнера ETL
    ├── elasticsearch_loader.py     # Модуль загрузки данных в ElasticSearch
    ├── etl_models.py               # Модели данных в ElasticSearch
    ├── postgres_extractor.py       # Модуль выгрузки данных из PostgreSQL
    ├── put_data_from_pg_to_es.py   # Основной скрипт ETL
    ├── requirements.txt            # Зависимости компонента ETL
    ├── run.sh                      # Скрипт, выполняемый при старте контейнера
    ├── sql_movies.py               # SQL скрипт для выгрузки данных из PostgreSQL
    ├── storage_config.py           # Модели конфигурации
    ├── utils.py                    # Вспомогательные функции
    
    
├── structure_migration/            # Миграции для создания структур данных с использованием Alembic
    ├── versions/                   # Миграции
    ├── env.py                      # Настройка окружения Alembic
    ├── script.py.mako              # Шаблон миграции Alembic
    
    
├── tests/                                  # Папка с комплектов тестов
    ├── functional/                         # Функциональные тесты
        ├── src                             # Папка с тестами
            ├── test_cache.py               # тесты кеширования
            ├── test_films.py               # тесты фильмов
            ├── test_films_content.py       # тесты данных из конкретных фильмов
            ├── test_genres_content.py      # тесты данных из конкретных жанров
            ├── test_get_last_element.py    # тесты работы последнего элемента
            ├── test_pagination.py          # тесты работы пагинации
            ├── test_persons_content.py     # тесты данных о конкретных персонах
            ├── test_sort.py                # тесты сортировки
        ├── testdata                        # Тестовые данные
            ├── es_data_collection.py       # Тестовые данные для наполнения elastic
        ├── utils                           # Утилиты
            ├── create_es_schema.sh         # файл создания индексов в elastic
            ├── entrypoint.sh               # файл для запуска тестов в контейнере
            ├── helpers.py                  # билиотека с доп процедурами
            ├── wait_for_es.py              # Тест на запуск elastic
            ├── wait_for_redis.py           # Тест на запуск redis
        ├── .env.example                    # Пример файла с переменными окружения
        ├── requirements.txt                # Зависимости для тестов
        ├── settings.py                     # Файл настроек


├── tests_auth/                             # Папка с комплектов тестов для AUTH сервиса
    ├── functional/                         # Функциональные тесты
        ├── src                             # Папка с тестами
            ├── test_flask_admin.py         # тесты административных API
            ├── test_flask_auth.py          # тесты пользовательских API
            ├── test_flask_ddos.py          # тесты ddos ручек API 
        ├── requirements.txt                # Зависимости для тестов
        ├── settings.py                     # Файл настроек
        ├── wait_for_flask.py               # Вейтер запуска flask
        ├── wait_for_keycloak.py            # Вейтер запуска KeyCloak
        ├── conftest.py                     # Хелперы


├── tests_analytic/                         # Папка с комплектов тестов для UTG-1
    ├── functional/                         # Функциональные тесты
        ├── src                             # Папка с тестами
            ├── test_add_ugc.py             # тесты добавления таймштампа на фильм
        ├── requirements.txt                # Зависимости для тестов
        ├── settings.py                     # Файл настроек
        ├── wait_for_fastapi.py             # Вейтер запуска FastAPI


├── nginx_config/                   # Папка с настройками nginx
    ├── conf.d/                     # Папка с настройками сайтов
        ├── site.conf               # Настройка для проекта fastapi
    ├── nginx.conf                  # Файо с общими настройками nginx


├── logstash/                       # Папка с настройками сервиса logstash
    ├── logstash.conf               # файл настроек сервиса logstash 
   
 
├── fluentd/                        # Папка с настройками сервиса fluentd
    ├── conf/                       # Папка с настройками сервиса
        ├── fluent.conf             # Файл настроек сервиса fluentd
    ├── Dockerfile                  # Dockerfile контейнера с установкой плагина GELF


├── rabbit_api/                     # Папка с FastAPI для API сервиса записи контента от 
                                      пользователей (лайки, обзоры, таймстампы, лайки обзорам)
    ├── mq/                        
        ├── conf/                   # Папка с настройками для rabbitmq
            ├── rabbitmq.conf       # сохранение пользователем места просмотра фильма
        ├── plugins/                # папка с плагинами
            ├── rabbitmq_delayed_message_exchange-3.12.0.ez    # плагин для корзины delay
        ├── requirements.txt        # файл с зависимостями для FastAPI
        ├── Dockerfile              # Dockerfile контейнера FastApi-solution
    ├── render/                        
        ├── src/                    # Папка с системой render 
        ├── requirements.txt        # файл с зависимостями для render
        ├── Dockerfile              # Dockerfile контейнера rabbit-render
    ├── sender/                        
        ├── src/                    # Папка с системой sender 
        ├── requirements.txt        # файл с зависимостями для render
        ├── Dockerfile              # Dockerfile контейнера rabbit-render

    
├── redis_config/                   # Папка с Redis Cache
    ├── redis.conf                  # Файл с настройками для Redis
    ├── Dockerfile                  # Dockerfile контейнера ETL


├── redis_config_ugc/               # Папка с настройками Redis Cache - UGC
    ├── redis.conf                  # Файл с настройками для Redis
    ├── Dockerfile                  # Dockerfile контейнера ETL


├── ugc_api/                        # Папка с FastAPI для API сервиса записи контента от 
                                      пользователей (лайки, обзоры, таймстампы, лайки обзорам)
    ├── api/                        
        ├── v1/                     # Папка с api версии 1
            ├── frame.py            # сохранение пользователем места просмотра фильма
            ├── like.py             # управление лайками
            ├── review.py           # управление обзорами
            ├── like_review.py      # управление лайками для обзоров
    ├── db/                         # папка с функциями для работы с mongo
        ├── mongo.py                # mongo consumer/producer 
    ├── models/                     # папка с файлами моделей
        ├── models.py               # файл со всеми моделями проекта   
    ├── main.py                     # основной файл запуска проекта
    ├── requirements.txt            # файл с зависимостями для FastAPI
    ├── Dockerfile                  # Dockerfile контейнера FastApi-solution
    ├── wait_for_mongo.py           # Вейтер для MongoDB
    ├── settings.py                 # Файл настроек


├── .env.example                    # Пример файла с переменными окружения
├── build_dev.bat                   # файл для сборки проекта под Windows
├── docker-compose.yml              # dev файл для сборки проекта в докере
├── docker-compose-logs.yml         # файл для сборки системы логгирования в докере
├── docker-compose-prod.yml         # product файл для сборки проекта в докере
├── docker-compose-tests.yml        # product файл для сборки проекта в докере
├── docker-compose-mongo-solo.yml   # компоуз для сборки системы mongo


├── setup.cfg                       # настройки flake8 и mypy
├── GITHUB_ACTION.md                # workflow github action
├── README.md
```


**Тонкости разворачивания проекта**

Для системы AUTH используется популярный сервис KeyCloak (https://www.keycloak.org/documentation),
сервис используется для авторизации и аутентификации. 
При разворачивании контейнеров, контейнер KeyCloak импортирует настройки из файла realm-export.json,
в нем сделаны базовые настройки для KeyCloak (создан realm Cinema, создан клиент Theatre, настроены
способы шифрования, способы авторизации, и т.п.)

Ссылка на библиотеку работы OAuth с российскими провайдерами
https://mvnrepository.com/artifact/ru.playa.keycloak/keycloak-russian-providers/1.0.49

**Сервисы и используемые порты**

|                  Docker-compose                  |       Контейнеры        |            Порт             |
|:------------------------------------------------:|:-----------------------:|:---------------------------:|
|            docker-compose-rabbit.yml             | db<br/>rabbit_api       | "5435:5432"<br/>"8001:8000" |
| docker-compose.yml<br/>docker-compose-tests.yml  |  fastapi_service<br/>   | "8000:8000"<br/>"5432:5432" |
 

**FlaskAPI**

Ссылка на документацию: http://localhost:8001/apidoc/swagger
Ссылка на схему с описанием контрактов: http://localhost:8001/apidoc/openapi.json
Функции реализованы в одном файле app.py, так как используемая библиотека для генерации документации
flask_pydantic_spec не поддерживает использование BluePrint
''

