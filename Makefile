.PHONY: requirements run

requirements:
	pip-compile
	pip-sync

run:
	cd hotasballs; lambda invoke -v