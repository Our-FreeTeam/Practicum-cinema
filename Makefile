run_rabbit:
	cp .env.example .env
	docker-compose -f docker-compose-rabbit.yml up --build -d
	sleep 20
	docker-compose -f docker-compose-sender.yml up --build -d