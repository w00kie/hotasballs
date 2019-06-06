.PHONY: requirements run deploy

requirements:
	pip-compile
	pip-sync

run:
	cd hotasballs; lambda invoke -v

deploy:
	cd hotasballs; lambda deploy