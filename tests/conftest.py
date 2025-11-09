import pytest

def pytest_runtest_call(item):
    if "cov" in item.keywords:
        # Enforce cov, but use CLI primarily
        pass