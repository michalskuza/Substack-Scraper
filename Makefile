.PHONY: help install install-dev test lint format type-check clean build upload docs

help:
	@echo "Substack Scraper - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install package and dependencies"
	@echo "  make install-dev      Install with development dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test            Run tests with coverage"
	@echo "  make lint            Run flake8 linter"
	@echo "  make format          Format code with black"
	@echo "  make type-check      Run mypy type checker"
	@echo "  make check           Run all checks (lint, format, type-check, test)"
	@echo ""
	@echo "Build:"
	@echo "  make clean           Clean build artifacts"
	@echo "  make build           Build distribution packages"
	@echo ""
	@echo "Other:"
	@echo "  make docs            Generate documentation"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt
	pip install -e .

test:
	pytest tests/ -v --cov=src/substack_scraper --cov-report=term-missing --cov-report=html

test-fast:
	pytest tests/ -v -x

lint:
	flake8 src/substack_scraper tests

format:
	black src/substack_scraper tests

format-check:
	black --check src/substack_scraper tests

type-check:
	mypy src/substack_scraper --ignore-missing-imports

check: lint format-check type-check test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf src/*.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

upload: build
	twine upload dist/*

upload-test: build
	twine upload --repository testpypi dist/*

docs:
	@echo "Documentation in README.md, CONTRIBUTING.md, and MIGRATION.md"
