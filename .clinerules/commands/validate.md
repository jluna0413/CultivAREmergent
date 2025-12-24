# Comprehensive Validation Command for CultivAR

This command orchestrates a full validation suite for the CultivAR application, covering code quality, unit tests, and end-to-end user workflows for both the FastAPI backend and the Flutter frontend.

## Usage

Run this command from the project root directory:

```bash
python .clinerules/commands/validate.md
```

## Phases

### Phase 1: Linting

Checks code style and potential issues using project-specific linters.

#### Python Backend (FastAPI/Flask)

```bash
echo "--- Running Pylint for Python backend ---"
pylint app/
echo "--- Running Flake8 for Python backend ---"
flake8 app/
```

#### Flutter Frontend

```bash
echo "--- Running Flutter Analyzer for Flutter frontend ---"
cd flutter_app && flutter analyze --no-pub && cd ..
```

### Phase 2: Type Checking

Verifies type consistency in the Python backend.

#### Python Backend (FastAPI/Flask)

```bash
echo "--- Running Mypy for Python backend ---"
mypy app/
```

### Phase 3: Style Checking

(No explicit style checking commands found for `black --check` or `prettier --check` in existing configurations. If a specific "check" command is implemented, it should be added here.)

### Phase 4: Unit Testing

Executes unit and widget tests for both backend and frontend.

#### Python Backend (FastAPI/Flask)

```bash
echo "--- Running Pytest for Python backend ---"
pytest
```

#### Flutter Frontend

```bash
echo "--- Running Flutter Unit and Widget Tests for Flutter frontend ---"
cd flutter_app && flutter test --no-pub --reporter expanded && cd ..
```

### Phase 5: End-to-End Testing (Comprehensive User Journeys)

Validates complete user workflows, API integrations, and frontend-backend interactions.

#### FastAPI Backend E2E Workflows

This runs a comprehensive E2E script that covers health checks, user registration, login, authenticated endpoint access, CRUD operations, file uploads, WebSocket connectivity, and error handling.

```bash
echo "--- Running FastAPI End-to-End Tests ---"
python comprehensive_e2e_test.py
```

#### Flutter Frontend Integration Tests

These tests validate the Flutter application's integration with the backend and overall user experience.

```bash
echo "--- Running Flutter Integration Tests ---"
cd flutter_app && flutter test integration_test --no-pub --reporter expanded && cd ..
```
