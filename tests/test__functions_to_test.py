"""
Assorted boilerplate tests demonstrating pytest syntax and use cases.
Documentation: https://docs.pytest.org/en/7.1.x/example/index.html
Reference:     https://github.com/mCodingLLC/clickThatLikeButton-TestingStarterProject?tab=readme-ov-file
"""

import sys
import time
import pytest

from datatools._functions_to_test import (
    LikeState, click_many,
    omit_string_patterns, imdb_film_retrieve, transpose_table,
)


# --- Test classes for encapsulating related beahviour / context sharing ---
# Reference: https://docs.pytest.org/en/7.1.x/getting-started.html

# Custom decorators
# Reference: https://docs.pytest.org/en/latest/how-to/mark.html#mark
@pytest.mark.slow
class TestFilmMetadata:
    # Shared context
    title = "spirited away"
    film_metadata = imdb_film_retrieve(title)

    # Testing expected behaviour
    def test_get_film_year(self):
        film_year = self.film_metadata["year"]
        assert film_year == 2001

    def test_get_film_director(self):
        film_director = self.film_metadata["director"][0]["name"]
        assert film_director == 'Hayao Miyazaki'


# --- Testing basic expected behaviour ---
def test_empty_click():
    assert click_many(LikeState.empty, '') is LikeState.empty


def test_single_clicks():
    assert click_many(LikeState.empty, 'l') is LikeState.liked
    assert click_many(LikeState.empty, 'd') is LikeState.disliked


# --- Parametrizing tests ---
# Reference: https://docs.pytest.org/en/7.1.x/example/parametrize.html
@pytest.mark.parametrize("test_input,expected", [
    ('ll', LikeState.empty),
    ('dd', LikeState.empty),
    ('ld', LikeState.disliked),
    ('dl', LikeState.liked),
    ('ldd', LikeState.empty),
    ('lldd', LikeState.empty),
    ('ddl', LikeState.liked),
])
def test_multi_clicks(test_input, expected):
    """A parametrized test.
    """
    assert click_many(LikeState.empty, test_input) is expected


# --- Error handling ---
# Reference: https://docs.pytest.org/en/7.1.x/how-to/skipping.html
# Expected failure
@pytest.mark.xfail
def test_divide_by_zero():
    assert 1 / 0 == 1


# Exceptions
def test_invalid_click():
    with pytest.raises(ValueError):
        click_many(LikeState.empty, 'x')


# --- Skipping tests ---
# Unconditional skip
@pytest.mark.skip(reason="regexes not supported yet")
def test_regex_clicks():
    assert click_many(LikeState.empty, '[ld]*ddl') is LikeState.liked


# Conditional skip
@pytest.mark.skipif(sys.version_info < (3, 11),
                    reason="requires python3.10 or higher")
def test_pytest_conditional_skipif():
    pass


# --- Using fixtures for context ---
# Session-wide database connection
# Reference: https://docs.pytest.org/en/7.4.x/reference/fixtures.html#fixture
@pytest.mark.xfail
def test_db_click(db_conn):
    db_conn.read_clicks()
    assert ...


# Testing printed output using a monkeypatch fixture
# Reference: https://docs.pytest.org/en/7.1.x/how-to/capture-stdout-stderr.html
def test_print(capture_stdout):
    print("hello")
    assert capture_stdout["stdout"] == "hello\n"
    

# --- Other testing patterns (e.g., text, tables) ---
def test_omit_string_patterns():
    input_string = "[[A \\\\ messy * string * with undesirable /patterns]]"
    patterns_to_omit = ["[[", "]]", "* ", "\\\\ ", "/", "messy ", "un"]
    output_string = omit_string_patterns(input_string, patterns_to_omit)
    assert output_string == "A string with desirable patterns"


def test_transpose_table():
    table = transpose_table([1, 2], [3, 4])
    assert list(table.iloc[0, :]) == ['31', '41']


# --- Benchmarking ---
# Reference: https://pytest-benchmark.readthedocs.io/en/latest/
# Useful: https://pytest-with-eric.com/pytest-best-practices/pytest-benchmark/
def something(duration=.0000001):
    """Function to be benchmarked. Accepts the seconds it will take to run.
    """
    time.sleep(duration)
    # Return anything, as in a normal test
    return 123


@pytest.mark.benchmark
def test_my_stuff(benchmark):
    """Benchmarking function.
    """
    # benchmark something
    result = benchmark(something)

    # Extra code to verify that the run completed correctly
    assert result == 123


# Encapsulate any to-be-benchmarked tests and pass to the benchmark fixture
# Limit rounds and time to make output more readable as needed
@pytest.mark.benchmark(
    min_rounds=5, 
    min_time=0.1,
    disable_gc=True,
    warmup=False,
)
def test_omit_benchmark(benchmark):
    """A standard benchmarking wrapper function.
    """
    benchmark(test_omit_string_patterns)
    


# --- Overview of useful pytesting CLI routines ---
# Documentation: https://docs.pytest.org/en/7.1.x/how-to/usage.html
# Reference: https://stackoverflow.com/questions/36456920/specify-which-pytest-tests-to-run-from-a-file
#
# Run the following after any of the below to produce a coverage report:
# (root_dir) $ coverage html && open htmlcov/index.html
#
# 1. Run all doctests in package {0 args + path}:
# Reference: https://docs.pytest.org/en/7.1.x/how-to/doctest.html
# Note: doctests must be run from the pkg directory.
#   Configurations in the root 'pyproject.toml' file won't be applied.
# (pkg_dir) $ coverage run -m pytest {path}/{module}.py --doctest-modules
#
# 2. Run all tests of a pkg (with tests stored in '{root}/tests/') {0 args}:
# (root_dir) $ coverage run -m pytest
#
# 3. Run tests of a particular {subpkg} {1 arg}:
# (root_dir) $ coverage run -m pytest tests/{subpkg}
#
# 4. Run tests of a particular {subpkg}/{module} {2 args / 1 path}:
# (root_dir) $ coverage run -m pytest tests/{subpkg}/test_{mod}.py
#
# 5. Run tests of a particular {path}/{test_function} {1 arg + path}:
# (root_dir) $ coverage run -m pytest tests/{path}.py::test_{func_testname}
#
# 6. Run tests of a particular {path}/{TestClass} {1 arg + path}:
# (root_dir) $ coverage run -m pytest tests/{path}.py::Test{ClassName}

# 7. Run tests of a particular {path}/{TestClass}.{test_meth} {2 args + path}:
# (root_dir) $ coverage -m pytest tests/{path}.py::{Class}::test_{meth_tstname}
#
# 8. Run all tests that have a particular marker {1 arg + path}:
# (root_dir) $ coverage run -m pytest tests/{path}.py -m {markername}
#
# 9. Run all tests other than those with a particular marker {1 arg + path}:
# (root_dir) $ coverage run -m pytest tests/{path}.py -m “not {markername}”
#
# 10. Run all tests that match a given {pattern} {1 arg + path}
# Note:
# Reference:
#
#
# --- Important preconditions for running pytest successfully ---
# Local importing syntax within package vs root directory:
# (pkg_dir) Use absolute imports relative to pkg: `(pkg){subpkg}.{module}`
# (root_dir) Use abs imports relative to src: `(src){pkg}.{subpkg}.{module}`

# Configure IDE workspace and launch protocols accordingly. See, e.g.:
# ‘(root).vscode/{data-tools.code-workspace, launch.json}’
# ‘(pkg).vscode/{pkg}.launch.json}’
