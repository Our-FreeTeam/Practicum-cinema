Проверка хранилища

docker-compose -f mongo/docker-compose.yml up  --build -d
docker-compose -f clickhouse/docker-compose.yml up  --build -d
pip install -r requirements.txt
