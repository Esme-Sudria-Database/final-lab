.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "Docker commands:"
	@echo "  start           Start all containers"
	@echo "  stop            Stop all containers"
	@echo "  populate-pg     Populate the PostgreSQL database"
	@echo "  populate-mongo  Populate the MongoDB database"
	@echo "  get-jupyter-token  Get the Jupyter token from the docker logs"
	@echo ""
	@echo "Utility commands:"
	@echo "  print           Print a hello message"
	@echo "  help            Show this help message"
	@echo "  generate-data   Generate data for the pgsql database"
	@echo ""


##@ Docker commands
.PHONY: start
start: ## Start all containers
	@docker compose up -d

.PHONY: stop
stop: ## Stop all containers
	@docker compose down

.PHONY: populate-pg
populate-pg: ## Populate the PostgreSQL database
	@docker compose exec -it esme_postgresql /data/load_dumps.sh

.PHONY: populate-mongo
populate-mongo: ## Populate the MongoDB database
	@docker compose exec -it esme_mongodb /esme_data/mongoimport.sh

.PHONY: get-jupyter-token
get-jupyter-token: ## Get the Jupyter token from the docker logs
	@docker compose logs esme_pyspark | grep "token=" | cut -d'=' -f2 | head -n 1

##@ Utility commands
.PHONY: print
print: ## Print a hello message
	@echo "hello from Makefile"

.PHONY: generate-data
generate-data: ## Generate data for the pgsql database
	@poetry shell && python3 generate_data/company_factory_data.py
	@poetry shell && python3 generate_data/sensor_factory_data.py
	@poetry shell && python3 generate_data/spark_sensors_data.py
	@cp generate_data/output/factories.sql.dump esme_postgresql/data/factories.sql.dump
	@cp generate_data/output/sensors.json esme_mongodb/esme_data/sensors.json
	@cp generate_data/output/sensors.sql.dump esme_postgresql/data/sensors.sql.dump