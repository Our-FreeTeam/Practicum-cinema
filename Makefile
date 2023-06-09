run_rabbit:
	cp rabbit_api/.env.example rabbit_api/src/.env
	cp rabbit_api/.env.example rabbit_api/render/.env
	cp rabbit_api/sender/.env.example rabbit_api/sender/.env
	docker-compose -f docker-compose-rabbit.yml up --build -d
	sleep 20
	docker-compose -f docker-compose-sender.yml up --build -d