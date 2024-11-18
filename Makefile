.PHONY: install test lint clean

install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/

lint:
	black .
	isort .
	flake8 .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +