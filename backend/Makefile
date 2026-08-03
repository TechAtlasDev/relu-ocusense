.PHONY: help install setup-env dev test clean

# Color output helpers
GREEN  := \033[0;32m
NC     := \033[0m

help: ## Muestra este mensaje de ayuda
	@echo "Uso: make <comando>"
	@echo ""
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  ${GREEN}%-15s${NC} %s\n", $$1, $$2}'

install: ## Instala todas las dependencias del proyecto con uv
	uv sync

setup-env: ## Crea el archivo .env a partir de .env.example si no existe
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		printf "${GREEN}.env creado desde .env.example${NC}\n"; \
	else \
		echo ".env ya existe"; \
	fi

dev: setup-env ## Ejecuta el bot de Telegram en modo desarrollo
	uv run python main.py

test: ## Ejecuta la suite de pruebas unitarias con pytest
	uv run pytest

clean: ## Elimina cachés de Python y entornos temporales
	rm -rf .pytest_cache __pycache__ app/__pycache__ app/*/__pycache__ tests/__pycache__
