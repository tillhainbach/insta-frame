.PHONY: check-porcelain deploy sync-requirements test

check-porcelain:
ifneq ($(shell git status --porcelain),)
	$(error "Working tree dirty!")
endif

deploy: check-porcelain sync-requirements
	git push heroku main

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
	./poetry run pytest --cov=insta_frame --cov-report html
