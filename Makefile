all:
	poetry run isort payment_webhook/ tests/
	poetry run black payment_webhook/ tests/
	poetry run flake8 payment_webhook/ tests/
	poetry run mypy payment_webhook/ tests/ --install-types --non-interactive --show-error-codes
	poetry run pylint payment_webhook/ tests/
	poetry run wily build payment_webhook/
	poetry run wily diff -a --no-detail payment_webhook/

style:
	isort payment_webhook/
	black --line-length 120 payment_webhook/

run:
	uvicorn payment_webhook.main:app --host 0.0.0.0 --port 8001 --reload
