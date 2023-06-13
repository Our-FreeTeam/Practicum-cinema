# Проверка хранилища

Для запуска тестирования скорости чтения и записи в хранилищах необходимо выполнить команды:
```
docker-compose -f mongo/docker-compose.yml up  --build -d
docker-compose -f clickhouse/docker-compose.yml up  --build -d
pip install -r requirements.txt
python -m data_storage_research
```

Результат представлен на графиках (синим цветом изображены результаты тестирования ClickHouse, оранжевым - MongoDB):
![insert_films.png](insert_films.png)
![insert_reviews.png](insert_reviews.png)
![insert_bookmarks.png](insert_bookmarks.png)

Чтение из БД:
![read.png](read.png)
