help:
	@echo manage
	@echo -e "\tmake manage createsuperuser -- --username admin"
	@echo -e "\tmake manage showmigrations"
	@echo
	@echo test
	@echo -e "\tmake test"
	@echo -e "\tmake test modules/api/tests/test_healthcheck.py::test_healthcheck_endpoint"
	@echo -e "\tmake test-cov && firefox backend/htmlcov/index.html"
	@echo
	@echo poetry
	@echo -e "\tmake poetry show -- -t"
	@echo -e "\tmake poetry show -- -o"
	@echo -e "\tmake poetry add pandas"
	@echo
	@echo scripts
	@echo -e "\tmake verify"
	@echo -e "\tmake run-black"
	@echo -e "\tmake run-fix-imports"

DOCKER_COMPOSE := $(shell which docker-compose 2> /dev/null)
ifndef DOCKER_COMPOSE
	DOCKER_COMPOSE := docker compose
endif

poetry:
	$(DOCKER_COMPOSE) run --rm -uroot backend poetry $(filter-out $@,$(MAKECMDGOALS))

manage:
	$(DOCKER_COMPOSE) exec backend python manage.py $(filter-out $@,$(MAKECMDGOALS))

test:
	$(DOCKER_COMPOSE) exec backend pytest $(filter-out $@,$(MAKECMDGOALS))

test-cov:
	$(DOCKER_COMPOSE) exec backend bash -c "pytest --cov=. --cov-report=html"

verify:
	$(DOCKER_COMPOSE) exec backend /scripts/run-verify

run-black:
	$(DOCKER_COMPOSE) exec backend /scripts/run-black

run-ruff:
	$(DOCKER_COMPOSE) exec backend /scripts/run-ruff

run-fix-imports:
	$(DOCKER_COMPOSE) exec backend /scripts/run-fix-imports

up:
	$(DOCKER_COMPOSE) up -d

logs:
	$(DOCKER_COMPOSE) logs -f $(filter-out $@,$(MAKECMDGOALS))

down:
	$(DOCKER_COMPOSE) down

%:
	@:
