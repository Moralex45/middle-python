SHELL := /bin/bash

run:
	python3 src/wsgi.py

flake8:
	flake8 "$(filter-out $@,$(MAKECMDGOALS))"

beautify:
	isort src
	autopep8 -r --in-place --aggressive --aggressive src

git:
	read -p "Check commit message, press any key to continue" -n1 -s
	git add .
	git commit -S -m "$(filter-out $@,$(MAKECMDGOALS))"

%:
	@:
