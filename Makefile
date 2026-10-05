.PHONY: help setup install db-up db-down db-seed train eval test lint run-api run-ui run clean

PYTHON ?= python
PIP ?= pip

help:
	@echo "Available commands:"
	@echo "  make setup        - Install dependencies and setup environment"
	@echo "  make db-up        - Start MySQL container"
	@echo "  make db-seed      - Load Olist data and generate synthetic layer"
	@echo "  make train        - Train customer segmentation, propensity, forecasting, and territory models"
	@echo "  make eval         - Run evaluation suite on golden questions and experiments"
	@echo "  make test         - Run pytest test suite"
	@echo "  make lint         - Run ruff code linter"
	@echo "  make run-api      - Launch FastAPI backend"
	@echo "  make run-ui       - Launch Streamlit interface"
	@echo "  make run          - Launch both API and UI"

setup:
	$(PIP) install -r requirements.txt
	@echo "Setup complete. Verify .env settings."

db-up:
	docker-compose up -d mysql

db-down:
	docker-compose down

db-seed:
	$(PYTHON) -m src.copilot.db.loader

train:
	$(PYTHON) -m src.copilot.models.segmentation
	$(PYTHON) -m src.copilot.models.propensity
	$(PYTHON) -m src.copilot.models.forecasting
	$(PYTHON) -m src.copilot.models.territory

eval:
	$(PYTHON) -m eval.run_eval
	$(PYTHON) -m eval.experiments

test:
	pytest -v tests/

lint:
	ruff check .

run-api:
	uvicorn src.copilot.api.main:app --host 0.0.0.0 --port 8000 --reload

run-ui:
	streamlit run src/copilot/ui/app.py

run:
	docker-compose up --build

clean:
	rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
