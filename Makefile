run_all_services:
	cp .env.example .env
	# Сервис логов
	docker-compose -f docker-compose-logs.yml up --build -d
	# БД монго
	docker-compose -f docker-compose-mongo-solo.yml up --build -d
	# БД монго
	docker-compose -f docker-compose-authsubsys.yml up --build -d
	# Запуск всех остальных сервисов
	docker-compose -f docker-compose.yml up --build -d

run_rabbit:
	cp .env.example .env
	docker-compose -f docker-compose-rabbit.yml up --build -d
	sleep 20
	docker-compose -f docker-compose-sender.yml up --build -d