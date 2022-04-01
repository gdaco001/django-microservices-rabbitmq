#All commands are intended to run on a "development" environment
build-api:
	docker build -f api_service/Dockerfile -t api_service:1.0 .
deploy-api:
	docker-compose --env-file .dev.env -f api_service/composes/api-service-dev/docker-compose.yml up -d
shutdown-api:
	docker-compose --env-file .dev.env -f api_service/composes/api-service-dev/docker-compose.yml down
build-stock:
	docker build -f stock_service/Dockerfile -t stock_service:1.0 .
deploy-stock:
	docker-compose --env-file .dev.env -f stock_service/composes/stock-service-dev/docker-compose.yml up -d
shutdown-stock:
	docker-compose --env-file .dev.env -f stock_service/composes/stock-service-dev/docker-compose.yml down
build-all:
	docker build -f api_service/Dockerfile -t api_service:1.0 .
	docker build -f stock_service/Dockerfile -t stock_service:1.0 .
deploy-all:
	docker-compose --env-file .dev.env -f api_service/composes/api-service-dev/docker-compose.yml up -d
	docker-compose --env-file .dev.env -f stock_service/composes/stock-service-dev/docker-compose.yml up -d
shutdown-all:
	docker-compose --env-file .dev.env -f stock_service/composes/stock-service-dev/docker-compose.yml down
	docker-compose --env-file .dev.env -f api_service/composes/api-service-dev/docker-compose.yml down
