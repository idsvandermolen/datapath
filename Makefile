.PHONY: help
help:  ## Show help messages for make targets
	@awk 'BEGIN {FS = ":.*?## "}; /^[^: ]+:.*?## / {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## Setup python .venv
	python3 -m venv .venv \
	&& .venv/bin/pip install --no-cache-dir --upgrade pip setuptools wheel \
	&& . .venv/bin/activate \
	&& poetry install

.PHONY: lint
lint: ## Lint python module
	@pylint datapath

.PHONY: test
test: ## Run test suite
	@pytest

.PHONY: build
build: lint test ## Build all targets
	@python3 -m build
