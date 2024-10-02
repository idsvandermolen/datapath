VERSION=$(shell poetry version --short)
TAG=v$(VERSION)

.PHONY: help
help:  ## Show help messages for make targets
	@awk 'BEGIN {FS = ":.*?## "}; /^[^: ]+:.*?## / {printf "\033[32m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: bootstrap
bootstrap: ## Setup python .venv
	uv python install 3.8 \
	&& uv python pin 3.8

.PHONY: lint
lint: ## Lint python module
	@ruff check

.PHONY: test
test: ## Run test suite
	@uv run pytest

.PHONY: build
build: lint test ## Build all targets
	@uv build

.PHONY: bump-patch
bump-patch: ## Bump patch version
	@poetry version patch

.PHONY: bump-minor
bump-minor: ## Bump minor version
	@poetry version minor

.PHONY: bump-major
bump-major: ## Bump major version
	@poetry version major

.PHONY: tag
tag:
	@git tag -m "Release $(TAG)" $(TAG)

.PHONY: release
release: tag ## Publish a release
	@git push origin $(TAG)
