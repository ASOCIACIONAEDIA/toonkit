.PHONY: help install test lint format clean build publish

help:  ## Mostrar ayuda
	@echo "Toonkit - Makefile"
	@echo ""
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependencias
	pip install -e ".[dev]"

test:  ## Ejecutar tests
	pytest -v

test-cov:  ## Tests con coverage
	pytest --cov=toonkit --cov-report=term-missing --cov-report=html

test-fast:  ## Tests rápidos (sin fuzz)
	pytest -v -m "not fuzz and not slow"

test-fuzz:  ## Solo fuzz tests
	pytest -v -m fuzz

lint:  ## Linter con ruff
	ruff check toonkit tests

format:  ## Formatear código
	black toonkit tests
	isort toonkit tests

type-check:  ## Verificar tipos con mypy
	mypy toonkit

quality:  ## Ejecutar todas las verificaciones de calidad
	$(MAKE) lint
	$(MAKE) format
	$(MAKE) type-check
	$(MAKE) test

clean:  ## Limpiar archivos temporales
	rm -rf build dist *.egg-info .pytest_cache .coverage htmlcov
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:  ## Build distribución para PyPI
	python -m build

publish-test:  ## Publicar a TestPyPI
	twine upload --repository testpypi dist/*

publish:  ## Publicar a PyPI (producción)
	twine upload dist/*

.DEFAULT_GOAL := help

