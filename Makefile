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

DOCKER := $(shell which docker 2> /dev/null)
ifndef DOCKER
	DOCKER := docker
endif

poetry:
	$(DOCKER) compose run --rm -uroot backend poetry $(filter-out $@,$(MAKECMDGOALS))

manage:
	$(DOCKER) compose exec backend python manage.py $(filter-out $@,$(MAKECMDGOALS))

test:
	$(DOCKER) compose exec backend pytest -s $(filter-out $@,$(MAKECMDGOALS)) --maxfail=1 -vvv

test-cov:
	$(DOCKER) compose exec backend bash -c "pytest --cov=. --cov-report=html"

verify:
	$(DOCKER) compose exec backend /scripts/run-verify

run-black:
	$(DOCKER) compose exec backend /scripts/run-black

run-ruff:
	$(DOCKER) compose exec backend /scripts/run-ruff

run-fix-imports:
	$(DOCKER) compose exec backend /scripts/run-fix-imports

up:
	$(DOCKER) compose up -d

logs:
	$(DOCKER) compose logs -f $(filter-out $@,$(MAKECMDGOALS))

down:
	$(DOCKER) compose down

%:
	@:
