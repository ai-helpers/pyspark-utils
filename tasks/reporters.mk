report-types: ## Generate the project mypy type report.
	poetry run mypy pyspark_utils/ tests/ > reports/mypy.txt || true

report-tests: ## Generate the project unit test report.
	poetry run pytest --junitxml=reports/pytest.xml --numprocesses="auto" tests/ || true

report-quality: ## Generate the project quality report.
	poetry run ruff check --output-format=json --output-file=reports/ruff.json pyspark_utils/ tests/ || true

report-security: ## Generate the project security report.
	poetry run bandit --recursive --format=json --output=reports/bandit.json pyspark_utils/ || true

report-coverage: ## Generate the project test coverage report.
	poetry run pytest --cov=. --cov-report=xml:reports/coverage.xml --numprocesses="auto" tests/ || true

reporters: report-types report-tests report-quality report-security report-coverage ## Run all the reporters.