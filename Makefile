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

# TODO
# make cicdocs (qa-suite > make -C docs {dtest -B > html} > make -C docs html)

# Synchronize versions in sub-requirements files with latest installations.
update-pinned-requirements:
	@echo "\n\n\ni / ii  Updating requirements lock file..."
	pip list --format=freeze > requirements_pip.txt
	
	@echo "\n\n\nii / ii  Updating requirements files..."
	@echo "=================================================================="
	@for suffix in $(suffixes); do \
		current_file=$$(echo requirements$${suffix}.txt); \
		if [ ! -f $${current_file} ]; then \
			echo "\nWarning: $${current_file} not found. Skipping.\n"; \
			continue; \
		fi; \
		make update-requirements-file SUFF=$${suffix}; \
	done
	@echo "All requirements synchronized.\n"

# Extract package names and versions from requirements.txt and then
# search/replace outdated lines in sub-requirements file with matching
# packages in requirements.txt.
update-requirements-file:
	@echo "> Checking requirements$(SUFF).txt..."
	@echo "------------------------------------------------------------------"
	@packages=$$(cat requirements_pip.txt); \
	\
	for package in $$packages; do \
		package_name=$$(echo $${package} | cut -d '=' -f1); \
		package_version=$$(echo $${package} | cut -d '=' -f3); \
		matched_line=$$(grep "^$${package_name}=" requirements$(SUFF).txt); \
		\
		if [ ! -z "$${matched_line}" ]; then \
			matched_version=$$(echo $${matched_line} | cut -d '=' -f3); \
			\
			if [ "$${package_version}" != "$${matched_version}" ]; then \
				echo "$${package_name} version mismatch. Updating:" \
				"v$${matched_version} -> v$${package_version}"; \
				sed -i '' "s|^$$package_name=.*|$${package_name}==$${package_version}|" requirements$(SUFF).txt; \
			fi; \
		fi; \
	done
	@echo "done."
	@echo "------------------------------------------------------------------"

# Default suffixes for updating sub-requirements files
suffixes ?= "" _dev _docs _optional

# TODO
# make upgrade-deps (conda update > make cicdocs > make update-reqs)


# SCRATCH
# 
# MAKE
# ----
# 
# √ pre-commit hook: pip check outdated
# √ make update-reqs (pip export > make update-pinned-requirements)
# ~make cicdocs (qa-suite > make -C docs {dtest -B > html} > make -C docs html)
# ~make upgrade-deps (conda update > make cicdocs > make update-reqs)
# 
# SCENARIOS
# ---------
# 
# IF NEED TO ADD DEP:
# add to conda env file
# make upgrade-deps
# 
# IF PRE-COMMIT HOOK SHOWS OUTDATED (FOR NON-PINNED DEP; RUN MANUALLY):
# make upgrade-deps (conda update > make cicdocs)
# 
# IF ERROR DURING UPGRADE-DEPS:
# pin latest working v of deps causing conflict in env + relevant deps file
# (until conflict resolved for forward compatibility)
