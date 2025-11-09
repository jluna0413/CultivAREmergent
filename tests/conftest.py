import pytest

@pytest.fixture(autouse=True)
def coverage_report():
    yield
    # Post-test: Run cov if needed, but use CLI for now
