# ==============================================================================
# Command line routines for development. To run a recipe run:
# 
# 	$ make {recipe-name}
# 
# Reference: https://makefiletutorial.com/#makefile-cookbook
# ==============================================================================


# Variables
PKG ?= datopy


doctests:
	python src/datopy/run_doctests.py

# Argument `mod` can be a path to a python module (relative PKG dir) or a dir
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
	@echo "\n\n\n1 / 4  Running doctests..."
	@echo "=========================="
	coverage run -m pytest src/$(PKG) --doctest-modules
	coverage report
	
	@echo "\n\n\n2 / 4  Running pytests..."
	@echo "========================="
	coverage run -m pytest
	coverage report
	
	@echo "\n\n\n3 / 4  Running type checking..."
	@echo "==============================="
	mypy src
	
	@echo "\n\n\n4 / 4  Running linting..."
	@echo "========================="
	flake8 src

cov-report:
	coverage html && open htmlcov/index.html