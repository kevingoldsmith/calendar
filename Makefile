lint: ; @for py in *.py; do echo "Linting $$py"; pylint -rn $$py; done

black:
	black .

mypy:
	mypy --disallow-untyped-defs .

list:
	@grep '^[^#[:space:]].*:' Makefile

all: black lint mypy
