format-sources: ## Format the project sources.
	poetry run ruff format pyspark_utils/ tests/

formatters: format-sources ## Run all the formatters.