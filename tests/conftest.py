"""
Pytest test configuration file containing boilerplate fixtures
for use with '_functions_to_test.py'.
"""

import pytest
import sys


# --- Monkeypatching ---
@pytest.fixture
def capture_stdout(monkeypatch):
    buffer = {"stdout": "", "write_calls": 0}

    def fake_write(s):
        buffer["stdout"] += s
        buffer["write_calls"] += 1

    monkeypatch.setattr(sys.stdout, 'write', fake_write)
    return buffer


# --- Database connection ---
@pytest.fixture(scope="session")
def db_conn():
    db = ...
    url = ...
    # connection will be torn down after all tests finish
    with db.connect(url) as conn:
        yield conn
