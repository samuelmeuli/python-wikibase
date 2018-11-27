init:
	git config core.hooksPath .hooks

test:
	poetry run pytest -s

format:
	poetry run black python_wikibase --line-length=100

lint:
	poetry run flake8 python_wikibase --max-line-length=100
