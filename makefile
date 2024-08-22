BRANCH_NAME := $(shell git branch --show-current)
CLEANED_BRANCH_NAME := $(shell echo $(BRANCH_NAME) | sed "s/DE-/DE_/g")

setup-environment:
	@echo "[ INFO ] Setting up environment for development"
	pip install poetry -q
	poetry install
	poetry shell

set-environment-variables:
	@echo "[ INFO ] Set environment variables in .env"
	set -a
	source .env


