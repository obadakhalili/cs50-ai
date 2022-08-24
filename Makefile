install:
	pipenv install

format:
	black --exclude .venv .

lint:
	flake8 --exclude .venv .
