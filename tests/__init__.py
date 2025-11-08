import os

# Ensure required env vars are set before any test module imports application code.
# This runs when the tests package is imported (happens before test modules are imported).
os.environ.setdefault("SECRET_KEY", "test-secret-key-please-change")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("TESTING", "1")