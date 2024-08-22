setup-environment:
	@echo "[ INFO ] Setting up environment for development"
	pip install poetry -q
	poetry install
	poetry shell

set-environment-variables:
	@echo "[ INFO ] Set environment variables in .env"
	set -a
	source .env


