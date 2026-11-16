# SRUN Authenticator Pro - Makefile
# "Talk is cheap. Show me the code." - Linus Torvalds

PYTHON = python3
PIP = pip3
DOCKER = docker
REPO_NAME = srun-authenticator
IMAGE_NAME = ghcr.io/claw-king/$(REPO_NAME)

.PHONY: help install test run clean docker-build docker-run lint

help:
	@echo "Available targets:"
	@echo "  install      Install dependencies"
	@echo "  test         Run unit tests"
	@echo "  lint         Run style checks (flake8)"
	@echo "  run          Run the authenticator locally"
	@echo "  docker-build Build the optimized Docker image"
	@echo "  docker-run   Run in a Docker container"
	@echo "  clean        Remove temporary files"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install flake8

test:
	$(PYTHON) test_srun.py

lint:
	flake8 srun_login_pro.py test_srun.py --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 srun_login_pro.py test_srun.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

run:
	$(PYTHON) srun_login_pro.py

docker-build:
	$(DOCKER) build -t $(REPO_NAME):latest -f Dockerfile.pro .

docker-run:
	$(DOCKER) run --rm --env-file .env $(REPO_NAME):latest

clean:
	rm -rf __pycache__ .pytest_cache *.pyc
	find . -type d -name "__pycache__" -exec rm -rf {} +
