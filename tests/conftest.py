import pytest

def pytest_configure(config):
    config.addinivalue_line("markers", "cov: marks tests for coverage")

@pytest.fixture(autouse=True)
def coverage_report():
    yield
    # Post-test: Run cov if needed, but use CLI for now
