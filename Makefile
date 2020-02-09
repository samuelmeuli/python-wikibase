MODULE_PATH="python_wikibase"

# Install dependencies and Git hooks
.PHONY: install
install:
	poetry install
	git config core.hooksPath .hooks

# Update dependencies
.PHONY: update
update:
	poetry update

# Run tests
.PHONY: test
test:
	poetry run pytest -s

# Format Python code using Black and isort
.PHONY: format
format:
	poetry run black ${MODULE_PATH} ${BLACK_FLAGS}
	poetry run isort ${MODULE_PATH} --recursive ${ISORT_FLAGS}

# Lint Python code using flake8
.PHONY: lint
lint:
	poetry run flake8 ${MODULE_PATH} --max-line-length=100
