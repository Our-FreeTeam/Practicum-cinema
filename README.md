# Дипломная работа - биллинг сервис для онлайнкинотеатра

Создаем систему биллинга, включающую в себя контроль прав пользователя доступа к платному контенту,
api сервис приема платежей, cron сервис который проверяет подходит ли срок автопродления у 
пользователя


Для разворачивания проекта использовать env.example и build_dev.bat,
Либо разворачивать по очереди
docker-compose-logs.yml,
docker-compose-mongo-solo.yml,
docker-compose-authsubsys.yml,
docker-compose-rabbit.yml,
docker-compose-sender.yml,
docker-compose-kafka.yml
docker-compose.yml
docker-compose-billing.yml,

Ссылка на репозиторий https://github.com/Our-FreeTeam/Practicum-cinema
Ссылка на Sentry https://our-freeteam.sentry.io/issues/




# Структура проекта
```
├── UML_schema/                     # Папка с архитектурой проекта в UML
    ├── billing_diplom/                        
        ├── billing_schema.png      # схема реализации дипломного Биллинг Сервиса
    ├── current/                        
        ├── c2-scheme.txt           # текущая - уровень C2


├── billing_cron_service/           # Сервис биллинга на базе cron
    ├── utils/                        
        ├── payment_prc.py          # модуль с abs классом для работы с платежами
        ├── put_user_to_queue.py    # модуль авто отправки пользователей на продление подписки
        ├── rabbit_connection.py    # модуль подключения к rabbit
        ├── settings.py             # файл импорта настроек
        ├── sql.py                  # sql скрипты для выбора пользователей под автоплатеж
        ├── yookassa_router.py      # скрипт трансляции подтверждения оплаты из внешного webhook в 
                                    # в эндпоинт add_2_step сервиса billing_serivce
    ├── crontab                     # файл настрое crontab для запуска 2х сервисов                
    ├── requirements.txt            # файл с зависимостями
    ├── Dockerfile                  # Dockerfile контейнера
    ├── run.sh                      # скрипт entrypoint 
            
        
├── billing_money_maker_service/    # Сервис биллинга на базе cron        
    
├── billing_notif_sender/           # Сервис отправки сообщения в очередь на отправку нотиф пользователю
       
├── billing_payment_separator/      # Сервис обработки данных полученных в Kafka из Yookassa

├── billing_role_activator/         # Сервис активации ролей пользователя

├── billing_service/                # Сервис Fast API с эндпойнтами биллинга
                
├── mailercron_service/             # 

├── flaskapi-solution/              # API сервис на Flask для авторизации и регистрации
    ├── views/                        
        ├── v1/                     # Папка с api версии 1
            ├── admin.py            # эндпойнты админа
            ├── auth.py             # эндпойнты регистрации-авторизации пользователей
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


├── keycloak/                       # Сервис управления доступом KeyCloak
    ├── import                      # 
        ├── realm-export.json       # файл с базовыми настройками сервиса KeyCloak, в т.ч. 
                                    # настройки Realm - Cinema и клиента Theatre с помощью 
                                    # которого будет подключатся Flask к KeyCloak
    ├── providers                   # папка с аддонами для импорта (провайдеры OAuth)
        ├── keycloak-russian-providers-1.0.49.jar  # файл с плагинами для RU сервисов
    ├── Dockerfile                  # Dockerfile контейнера KeyCloak


├── fastapi-solution/               # Основной сервис онлайн кинотеатра получение информации о 
                                    # фильмах, актерах, поиск фильмов и т.п. На FastAPI
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
       

├── db/                             # Исходные данные с фильмами, актерами итп
    ├── models.py                   # Модели SQLAlchemy
    ├── movies_dataclasses.py       # Датаклассы для переливки данных из SQLite в PostgreSQL
    
    
├── etl/                            # ETL скрипты для перелива информации из PG в Elastic
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
    
    
├── tests/                                  # Комплект тестов для сервиса онлайн кинотеарта
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


├── tests_auth/                             # Комплект тестов для Flask AUTH сервиса
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


├── tests_analytic/                         # Комплект тестов для UTG-1 API сервиса
    ├── functional/                         # Функциональные тесты
        ├── src                             # Папка с тестами
            ├── test_add_ugc.py             # тесты добавления таймштампа на фильм
        ├── requirements.txt                # Зависимости для тестов
        ├── settings.py                     # Файл настроек
        ├── wait_for_fastapi.py             # Вейтер запуска FastAPI


├── nginx_config/                   # Nginx сервис для проекта
    ├── conf.d/                     # Папка с настройками сайтов
        ├── site.conf               # Настройка для проекта fastapi
    ├── nginx.conf                  # Файо с общими настройками nginx


├── logstash/                       # Logstash сервис
    ├── logstash.conf               # файл настроек сервиса logstash 
   
 
├── fluentd/                        # Fluentd сервис
    ├── conf/                       # Папка с настройками сервиса
        ├── fluent.conf             # Файл настроек сервиса fluentd
    ├── Dockerfile                  # Dockerfile контейнера с установкой плагина GELF


├── rabbit_api/                     # Сервис UGC API (FastAPI) для работы с контентом от 
                                    # пользователей (лайки, обзоры, таймстампы, лайки обзорам)
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

    
├── redis_config/                   # RedisCache кеширования запросов к Elastic с фильмами и т.п.
    ├── redis.conf                  # Файл с настройками для Redis
    ├── Dockerfile                  # Dockerfile контейнера ETL


├── redis_config_ugc/               # RedisCache UGC сервис кеширования данных от пользоватеоей
    ├── redis.conf                  # Файл с настройками для Redis
    ├── Dockerfile                  # Dockerfile контейнера ETL


├── ugc_api/                        # UGC Api сервис на FastAPI для работы с контентом от 
                                    # пользователей (лайки, обзоры, таймстампы, лайки обзорам)
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
├── docker-compose.yml              # dev файл для сборки ядра проекта 
├── docker-compose-authsubsys.yml   # сборка системы Auth 
├── docker-compose-logs.yml         # сборка системы логгирования 
├── docker-compose-rabbit.yml       # сборка системы очереди на Rabbit
├── docker-compose-sender.yml       # сборка системы почтовой рассылки 
├── docker-compose-mongo-solo.yml   # сборка системы mongo

├── docker-compose-tests.yml        # product файл для сборки проекта в докере

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
| docker-compose.yml  |  billing_cron_service<br/>   | "8010:8000"<br/>"5438:5432" |
 

**FlaskAPI**

Ссылка на документацию: http://localhost:8001/apidoc/swagger
Ссылка на схему с описанием контрактов: http://localhost:8001/apidoc/openapi.json
Функции реализованы в одном файле app.py, так как используемая библиотека для генерации документации
flask_pydantic_spec не поддерживает использование BluePrint
''

