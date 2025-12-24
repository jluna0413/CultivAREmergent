---
description: Comprehensive validation for CultivAR multi-platform application
---

# CultivAR Validation Suite

This command validates the entire CultivAR application stack including Python backend, Flutter frontend, database operations, and deployment configurations.

## Phase 1: Python Backend Linting & Type Checking

```bash
# Install Python dependencies
pip install -r requirements.txt

# Lint with pyflakes (CI standard)
pyflakes app tests

# Run type checking with mypy (if configured)
# mypy app tests  # Add mypy to requirements.txt if needed

# Check code formatting with black (if configured)
# black --check app tests
```

## Phase 2: Python Backend Unit Testing

```bash
# Run all Python tests
pytest tests/ --tb=short

# Run FastAPI-specific tests
pytest tests/test_fastapi_*.py

# Run Flask-specific tests (excluding FastAPI tests)
pytest tests/test_*.py -k 'not fastapi'

# Run with coverage
pytest tests/ --cov=app --cov-report=html --cov-report=term
```

## Phase 3: Flutter Code Analysis & Formatting

```bash
cd flutter_app

# Get dependencies
flutter pub get

# Check code formatting
dart format --output=none --set-exit-if-changed .

# Run static analysis
flutter analyze

# Run custom lints (if configured)
# flutter pub run custom_lint
```

## Phase 4: Flutter Code Generation Validation

```bash
cd flutter_app

# Generate code (Freezed, JSON serializable, Riverpod)
flutter pub run build_runner build --delete-conflicting-outputs

# Verify generated files exist and are valid
# Check for common generation issues
find lib -name "*.freezed.dart" -o -name "*.g.dart" | head -10
```

## Phase 5: Flutter Unit & Widget Testing

```bash
cd flutter_app

# Run all tests with coverage
flutter test --coverage

# Run specific test files
flutter test test/unit/models/
flutter test test/widget/

# Generate coverage report
genhtml coverage/lcov.info -o coverage/html
```

## Phase 6: Flutter Integration Testing

```bash
cd flutter_app

# Run integration tests (requires device/emulator)
flutter test integration_test/

# Run on specific device
flutter test integration_test/ -d emulator-5554
```

## Phase 7: Database & Migration Testing

```bash
# Test database connections and migrations
python scripts/verify_migration.py

# Run migration parity tests
pytest tests/test_migration_parity.py

# Test database operations
python -c "
import app
from app.database import get_db
db = next(get_db())
print('Database connection successful')
"
```

## Phase 8: API Integration Testing

```bash
# Start FastAPI server in background
python run_fastapi.py &
SERVER_PID=$!

# Wait for server to start
sleep 5

# Test API endpoints
curl -f http://localhost:8000/docs || echo "FastAPI docs not accessible"
curl -f http://localhost:8000/health || echo "Health check failed"

# Test authentication endpoints
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}' || echo "Auth test failed"

# Kill server
kill $SERVER_PID
```

## Phase 9: Docker Build Validation

```bash
# Test FastAPI Docker build
docker compose -f docker-compose.fastapi.yml build

# Test dual-stack Docker build
docker compose -f docker-compose.dual.yml build

# Test container startup
docker compose -f docker-compose.fastapi.yml up -d
sleep 10
curl -f http://localhost:8000/health || echo "Container health check failed"
docker compose -f docker-compose.fastapi.yml down
```

## Phase 10: Flutter Build Validation

```bash
cd flutter_app

# Build for web
flutter build web --release

# Build Android APK
flutter build apk --release

# Build iOS (if on macOS)
# flutter build ios --release

# Build Windows (if on Windows)
flutter build windows --release

# Build Linux (if on Linux)
flutter build linux --release
```

## Phase 11: End-to-End User Journey Testing

### Backend User Journeys

```bash
# Start FastAPI server
python run_fastapi.py &
SERVER_PID=$!

sleep 5

# 1. User Registration & Authentication
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass123"}'

TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' | jq -r '.access_token')

# 2. Plant Management Journey
# Create a plant
curl -X POST http://localhost:8000/plants/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Plant","strain_id":1,"status":"germinating"}'

# List plants
curl -X GET http://localhost:8000/plants/ \
  -H "Authorization: Bearer $TOKEN"

# 3. Strain Management Journey
curl -X GET http://localhost:8000/strains/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Sensor Data Journey
curl -X GET http://localhost:8000/sensors/data \
  -H "Authorization: Bearer $TOKEN"

# Clean up
kill $SERVER_PID
```

### Flutter User Journeys

```bash
cd flutter_app

# 1. Authentication Flow
# (Requires running Flutter app with integration tests)
flutter test integration_test/auth_flow_test.dart

# 2. Plant Management Flow
flutter test integration_test/plant_management_test.dart

# 3. Offline Functionality
flutter test integration_test/offline_test.dart

# 4. Sensor Data Visualization
flutter test integration_test/sensor_data_test.dart
```

## Phase 12: Performance & Load Testing

```bash
# Install locust or alternative load testing tool
# pip install locust

# Run load tests
# locust -f tests/load_tests.py --host=http://localhost:8000

# Memory leak detection for Flutter
cd flutter_app
flutter run --profile --trace-startup
```

## Phase 13: Security Validation

```bash
# Run security audit
pip install safety
safety check

# Test security headers
python test_security_headers.py

# Run vulnerability scans
# (Add tools like bandit, semgrep if configured)
```

## Phase 14: Deployment Validation

```bash
# Test production Docker builds
docker build -f Dockerfile.prod .

# Validate environment configurations
python -c "
import os
required_env = ['SECRET_KEY', 'DATABASE_URL']
for env in required_env:
    if not os.getenv(env):
        print(f'Missing required env: {env}')
"

# Test deployment scripts
bash scripts/deploy.sh --dry-run
```

## Phase 15: Cross-Platform Compatibility

```bash
# Test on multiple Python versions (if using pyenv/tox)
# tox

# Test Flutter on multiple platforms
cd flutter_app

# Web compatibility
flutter run -d chrome --release

# Mobile compatibility (requires devices/emulators)
# flutter run -d android
# flutter run -d ios
```

## Quick Validation Commands

### For Backend Development
```bash
make test-fastapi
pyflakes app tests
```

### For Flutter Development
```bash
cd flutter_app
flutter analyze
flutter test
flutter pub run build_runner build --delete-conflicting-outputs
```

### For Full CI Simulation
```bash
# Python checks
make test-all
pyflakes app tests

# Flutter checks
cd flutter_app
flutter pub get
dart format --output=none --set-exit-if-changed .
flutter analyze
flutter pub run build_runner build --delete-conflicting-outputs
flutter test --coverage

# Docker checks
docker compose -f docker-compose.fastapi.yml build
```

## Validation Status Reporting

After running validation, generate reports:

```bash
# Generate combined coverage report
cd flutter_app
genhtml coverage/lcov.info -o coverage/html

# Create validation summary
echo "=== VALIDATION SUMMARY ===" > validation_report.md
echo "Python Tests: $(pytest --collect-only 2>/dev/null | grep -c "test session starts") tests collected" >> validation_report.md
echo "Flutter Tests: $(find test -name "*.dart" | wc -l) test files" >> validation_report.md
echo "Coverage: Check coverage/html/index.html" >> validation_report.md
echo "Analysis: $(flutter analyze 2>&1 | grep -c "error") errors found" >> validation_report.md
```</content>
<parameter name="filePath">a:\dev\CultivAREmergant\.claude\commands\validate.md