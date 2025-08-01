.PHONY: run test clean lint format

run:
	@echo "Setting up virtual environment..."
	python -m venv venv
	@echo "Activating virtual environment..."
	venv\Scripts\activate
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Running Rubik's Cube Solver..."
	python main.py

test:
	@echo "Running tests..."
	pytest tests

lint:
	@echo "Linting with flake8..."
	flake8 lib main.py

format:
	@echo "Formatting with black..."
	black lib main.py

clean:
	@echo "Cleaning up __pycache__ and .pyc files..."
	@find . -type d -name "__pycache__" -exec rmdir /s /q {} + 2>nul || exit 0
	@del /s /q *.pyc 2>nul || exit 0