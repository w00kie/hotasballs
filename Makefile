.PHONY: project-requirements requirements run deploy

project-requirements:
	cd hotasballs; pip-compile --no-annotate

requirements: project-requirements
	pip-compile
	pip-sync

run:
	cd hotasballs; lambda invoke -v

deploy:
	cd hotasballs; lambda deploy --requirements requirements.txt