BUILDSTAMP=$(shell date -u '+%Y-%m-%d-%I-%M-%S%p')
PROJECT?=anime-ml
PYTHON = python3

setup:

	@echo "Running setup" \

	&& brew update \
	&& brew install pyenv \
	&& pyenv install ${cat .python-version} \
	&& python -m venv venv \
	&& source venv/bin/activate \
	&& pip install ./ \
	&& pip install black==20.8b1 pre-commit==2.8.2 isort==5.6.4 mypy==0.790
	&& pre-commit install


run:

	@echo "Running" \

	&& python anime_ml/cli.py
