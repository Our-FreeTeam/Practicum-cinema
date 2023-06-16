docker-compose -f docker-compose-logs.yml up -d
sleep 10
docker-compose -f docker-compose-mongo.yml up -d
sleep 10
docker-compose -f docker-compose-kafka.yml up -d
sleep 10
docker-compose -f docker-compose.yml up -d