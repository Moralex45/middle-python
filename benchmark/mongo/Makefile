## ----------------------------------------------------------------------
## The purpose of this Makefile is to manage MongoDB tests.
## ----------------------------------------------------------------------
compose_files=-f mongo-docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Launching the project infrastructure.
		docker-compose $(compose_files) up -d --build
stop:  ## Stop project.
		docker-compose $(compose_files) down

status:  ## Get docker containers status
		docker-compose $(compose_files) ps

db-init:  ## Configure Mongo cluster and create database UGC_data
		./rs-init.sh

full-test:  ## Run full tests
		pytest ./tests/mongo_test.py -vvs --durations=0

read-tests:  ## Run read only tests
		pytest ./tests/mongo_test.py -vvs -k 'not insert' --durations=0