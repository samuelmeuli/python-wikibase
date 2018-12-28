# Install dependencies and Git hooks
.PHONY: install
install:
	poetry install
	git config core.hooksPath .hooks

# Run tests
.PHONY: test
test:
	poetry run pytest -s

# Format Python code using Black
.PHONY: format
format:
	poetry run black python_wikibase --line-length=100 ${BLACK_FLAGS}

# Lint Python code using flake8
.PHONY: lint
lint:
	poetry run flake8 python_wikibase --max-line-length=100
