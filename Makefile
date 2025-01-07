.PHONY: help
help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "Docker commands:"
	@echo "  start           Start all containers"
	@echo "  stop            Stop all containers"
	@echo ""
	@echo "Utility commands:"
	@echo "  print           Print a hello message"
	@echo "  help            Show this help message"
	@echo ""


##@ Docker commands
.PHONY: start
start: ## Start all containers
	docker compose up -d

.PHONY: stop
stop: ## Stop all containers
	docker compose down

.PHONY: populate-pg
populate-pg: ## Populate the PostgreSQL database
	docker compose exec -it esme_postgresql /data/load_dumps.sh

.PHONY: populate-mongo
populate-mongo: ## Populate the MongoDB database
	docker compose exec -it esme_mongodb /esme_data/mongoimport.sh

##@ Utility commands
.PHONY: print
print: ## Print a hello message
	@echo "hello from Makefile"
