default: lint

isort:
	isort ./fastapi_issue_tracker

black:
	black ./fastapi_issue_tracker

flake:
	flake8 ./fastapi_issue_tracker

mypy:
	mypy --pretty ./fastapi_issue_tracker

lint:  isort black flake mypy
