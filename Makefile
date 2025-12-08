.PHONY: up down build logs restart run-flask run-fastapi docker-flask docker-fastapi docker-dual test-flask test-fastapi test-all docs-fastapi install-deps

# Run Flask application locally
run-flask:
	python run_flask.py

# Run FastAPI application locally
run-fastapi:
	python run_fastapi.py

# Run Flask application in Docker from dual-stack compose file
docker-flask:
	docker compose -f docker-compose.dual.yml up -d cultivar_flask --build

# Run FastAPI application in Docker
docker-fastapi:
	docker compose -f docker-compose.fastapi.yml up -d --build

# Run both Flask and FastAPI applications in Docker
docker-dual:
	docker compose -f docker-compose.dual.yml up -d --build

# Run FastAPI application in Docker with PostgreSQL
docker-fastapi-db:
	docker compose -f docker-compose.fastapi.yml up -d --build

# Run Flask-specific tests
test-flask:
	pytest tests/test_*.py -k 'not fastapi'

# Run FastAPI-specific tests
test-fastapi:
	pytest tests/test_fastapi_*.py

# Run all tests
test-all:
	pytest tests/

# Run migration verification script
verify:
	python scripts/verify_migration.py

# Run migration parity tests
test-parity:
	pytest tests/test_migration_parity.py

# Run CI smoke tests locally using act
ci-smoke:
	act -j smoke

# Open FastAPI documentation in browser
docs-fastapi:
	@echo "Opening FastAPI docs at http://localhost:8000/docs"
	@if command -v xdg-open > /dev/null; then \
		xdg-open http://localhost:8000/docs; \
	elif command -v open > /dev/null; then \
		open http://localhost:8000/docs; \
	else \
		echo "Please open http://localhost:8000/docs in your browser"; \
	fi

# Install all dependencies
install-deps:
	pip install -r requirements.txt

# Start the FastAPI application in Docker
up:
	docker compose -f docker-compose.fastapi.yml up -d --build

# Stop the FastAPI application in Docker
down:
	docker compose -f docker-compose.fastapi.yml down

# Build the FastAPI Docker image
build:
	docker compose -f docker-compose.fastapi.yml build --no-cache

# View logs for the FastAPI application in Docker
logs:
	docker compose -f docker-compose.fastapi.yml logs -f

# Restart the FastAPI application in Docker
restart:
	docker compose -f docker-compose.fastapi.yml restart