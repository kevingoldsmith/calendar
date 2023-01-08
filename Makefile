lint:
	pylint *.py

black:
	black .

mypy:
	mypy --disallow-untyped-defs .

all: lint black mypy
