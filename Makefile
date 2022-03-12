.PHONY: check-porcelain deploy lint show-coverage-report sync-requirements test

POETRY_VERSION=1.1

bootstrap: shim-poetry
	./poetry config virtualenvs.in-project true
	./poetry install

check-porcelain:
ifneq ($(shell git status --porcelain),)
	$(error "Working tree dirty!")
endif

deploy: check-porcelain sync-requirements
	git push heroku main

lint:
	./poetry run python -m flake8
	./poetry run python -m black --check .

require-poetry:
ifneq ($(findstring $(POETRY_VERSION),$(shell poetry --version)), $(POETRY_VERSION))
	$(info Install the latest version of poetry!)
	curl -sSL https://install.python-poetry.org | python -
endif

shim-poetry: require-poetry
	echo '$(shell which poetry) $$@' > ./poetry
	chmod +x ./poetry

show-coverage-report:
	open htmlcov/index.html

sync-requirements:
	echo "# This is generated automatically. Do not change!\n$$(./poetry export)" > requirements.txt
ifeq ($(findstring requirements.txt,$(shell git status --porcelain)), requirements.txt)
	@echo "Committing requirements.txt..."
	git add requirements.txt
	git commit -m "chore(web-app): sync requirements.txt with poetry" --no-verify
endif

test:
	./poetry run pytest $(extra-args)

test-cov:
	./poetry run pytest --cov=insta_frame --cov-report $(report-type)
