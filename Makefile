.PHONY: check-porcelain deploy sync-requirements

check-porcelain:
ifneq ($(shell git status --porcelain),)
	$(error "Working tree dirty!")
endif

deploy: check-porcelain sync-requirements
	git push heroku main

sync-requirements:
	echo "# This is generated automatically. Do not change!\n$$(./poetry export)" > requirements.txt
ifeq ($(shell git status --porcelain), M requirements.txt)
	git add requirements.txt
	git commit -m "chore(web-app): sync requirements.txt with poetry" --no-verify
endif
