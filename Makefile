freeze:
	touch requirements.txt && pipdeptree --warn silence | grep -E '^\w+' > requirements.txt

freeze-lock:
	touch requirements-lock.txt && pipdeptree > requirements-lock.txt

install: requirements.txt
	pip install -r requirements.txt

format:
	black --exclude .venv .

lint:
	flake8 --exclude .venv .
