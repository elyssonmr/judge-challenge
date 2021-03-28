install-prod:
	pip install -r requirements/requirements.txt

install-dev:
	pip install -r requirements/requirements_dev.txt

test:
	pytest -x judge
