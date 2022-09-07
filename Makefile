SHELL := /bin/bash

git:
	read -p "Check commit message, press any key to continue" -n1 -s
	git add .
	git commit -S -m "$(filter-out $@,$(MAKECMDGOALS))"

%:
	@:
