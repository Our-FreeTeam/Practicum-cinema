docker-compose -f docker-compose-logs.yml up -d
sleep 10
docker-compose -f docker-compose-mongo-solo.yml up -d
sleep 10
docker-compose -f docker-compose.yml up -d
sleep 10
docker-compose -f docker-compose-rabbit.yml up -d
sleep 10
docker-compose -f docker-compose-sender.yml up -d