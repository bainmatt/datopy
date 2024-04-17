# ==============================================================================
# Command line routines for development. To run a recipe run:
# 
# 	$ make {recipe-name}
# 
# ==============================================================================


# Globals
PKG ?= datatools


doctests:
	python src/datatools/run_doctests.py

# First arg `mod` can be a path to a python module (relative PKG dir) or a dir
py-doctests:
ifeq ($(mod),)
	@echo "\n\nNo subpackage or module specified. Running all doctests."
	coverage run -m pytest -vv src/$(PKG) --doctest-modules
else
	coverage run -m pytest -vv src/$(PKG)/$(mod) --doctest-modules
endif
	coverage report

pytests:
	coverage run -m pytest
	coverage report

qa-suite:
	@echo "\n\nRunning pytests\n===================="
	coverage run -m pytest
	coverage report
	@echo "\n\nRunning type checking\n===================="
	mypy src
	@echo "\n\nRunning linting\n===================="
	flake8 src

cov-report:
	coverage html && open htmlcov/index.html