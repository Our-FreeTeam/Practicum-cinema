docker-compose -f docker-compose-logs.yml up -d
timeout 10
docker-compose -f docker-compose-authsubsys.yml up -d
timeout 10
docker-compose -f docker-compose-mongo-solo.yml up -d
timeout 10
docker-compose -f docker-compose-rabbit.yml up -d
timeout 10
docker-compose -f docker-compose-sender.yml up -d
timeout 10
docker-compose -f docker-compose-kafka.yml up -d
timeout 10
docker-compose -f docker-compose.yml up -d
timeout 10
docker-compose -f docker-compose-billing.yml up -d
