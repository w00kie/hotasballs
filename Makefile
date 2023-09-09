.PHONY: all project-requirements requirements run deploy test \
	clean clean-pyc clean-build clean-requirements check-updates \
	update-requirements

all: requirements

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

clean-build:
	rm --force --recursive hotasballs/dist/

clean: clean-pyc clean-build

project-requirements:
	cd hotasballs; pip-compile --no-annotate

requirements: project-requirements
	pip-compile

check-updates:
	pip-compile -nU | diff requirements.txt -

clean-requirements:
	find . -name 'requirements.txt' -exec rm --force {} +

update-requirements: clean-requirements all

run:
	cd hotasballs; lambda invoke -v

test: clean-pyc
	python -m green -vvv
