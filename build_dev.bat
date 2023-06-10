docker-compose -f docker-compose-logs.yml up -d
docker-compose -f docker-compose-clickhouse.yml up -d
docker-compose -f docker-compose-kafka.yml up -d
docker-compose -f docker-compose.yml up -d