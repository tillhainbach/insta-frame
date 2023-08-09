.PHONY: check-porcelain deploy lint show-coverage-report test

POETRY_VERSION=1.5.1

bootstrap: shim-poetry
	./poetry config virtualenvs.in-project true
	./poetry install
	./poetry run pre-commit install

check-porcelain:
ifneq ($(shell git status --porcelain),)
	$(error "Working tree dirty!")
endif

deploy: check-porcelain
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

test:
	./poetry run pytest $(extra-args)

test-cov:
	./poetry run pytest --cov=insta_frame --cov-report $(report-type)

start:
	SECRET_KEY='secret' QUART_APP="insta_frame:create_app()" ./poetry run quart run

build:
	docker build . -t insta-frame

run:
	docker run --rm --env SECRET_KEY=abc -p 8080:8080 insta-frame
