freeze:
	touch requirements.txt && pip-chill > requirements.txt

install: requirements.txt
	pip install -r requirements.txt

format:
	yapf --exclude .venv --recursive --in-place .

lint:
	flake8 --exclude .venv .
