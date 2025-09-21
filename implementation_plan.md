# Implementation plan & roadmap (short)

This document captures the recent containerization work, the immediate next tasks, and how to sync this to Byterover/Archon if needed.

1. Containerization (done)
   - Added `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `Makefile`, and `README_DOCKER.md`.
   - Dev compose runs Flask with `--reload` and mounts the repo for hot-reload while developing the marketing frontend.
   - Dev `SECRET_KEY` is set in `docker-compose.yml` for local convenience — do NOT use this value in production.

2. Smoke tests (done)
   - Verified `/marketing/download/test` returns a PDF attachment and saved it locally via `curl`.

3. Lint & small refactors (in this commit)
   - Refactored `app/blueprints/marketing.py`:
     - Moved optional email validator import to module top.
     - Extracted helpers `_validate_email_address`, `_has_recent_download`, `_record_download_and_increment`, `_serve_lead_magnet_file`.
     - Replaced in-function imports and narrowed exception scopes where safe.
   - Ran `pylint` on the module — score improved. More lints remain (style/line length/complexity) to address incrementally.

4. Next high-priority tasks
   - Address runtime-impacting lints across the app (imports inside functions, broad excepts).
   - Add a CI GitHub Actions workflow to build and smoke-test the Docker image on push.
   - Add a dev bootstrap script (PowerShell) to start `docker compose up -d` on developer machines (optional).
   - Review long functions in `marketing.py` and split where appropriate to reduce complexity warnings.

5. Byterover / Archon sync
   - I couldn't access the project's Byterover storage tools from this environment, so I added this `IMPLEMENTATION_PLAN.md` file to the repo.
   - To sync with Byterover manually:
     1. Log into your Byterover/Archon dashboard.
     2. Create a new implementation plan entry titled "Containerize backend + linting".
     3. Paste the contents of this file and mark tasks as in-progress/completed as appropriate.

6. How to run locally (short)
   - Create a `.env` with a secure `SECRET_KEY` for dev.
   - PowerShell commands:

```powershell
# create env (one-time)
@"
SECRET_KEY=dev-secret-change-me
FLASK_ENV=development
FLASK_DEBUG=1
"@ > .env

# start in background
docker compose up -d --build

# logs
docker compose logs -f

# stop
docker compose down
```

7. Commit note
   - This commit includes the containerization files and the targeted refactor to `marketing.py` to reduce runtime issues and improve maintainability.
# CultivAR Implementation Plan

## Overview
This plan outlines the steps needed to transform the current basic implementation into an exact clone of the Isley project.

## 1. Complete Missing Templates

### 1.1 Plant Management
- Create plant list view
- Create plant detail view
- Create plant add/edit forms
- Implement plant activity tracking
- Implement plant image uploads

### 1.2 Strain Management
- Create strain list view
- Create strain detail view
- Create strain add/edit forms
- Implement seed inventory tracking

### 1.3 Sensor Management
- Create sensor list view
- Create sensor configuration view
- Create sensor data visualization
- Implement sensor scanning functionality

### 1.4 Settings
- Create settings view
- Implement configuration options
- Add zone management
- Add activity type management
- Add measurement type management

## 2. Implement Missing Functionality

### 2.1 Plant Tracking
- Complete plant lifecycle management
- Implement status transitions
- Add activity recording (watering, feeding, etc.)
- Add measurement recording (height, pH, etc.)

### 2.2 Sensor Integration
- Complete AC Infinity integration
- Complete Ecowitt integration
- Implement data collection and storage
- Add data visualization with charts

### 2.3 Image Management
- Implement image upload functionality
- Add image gallery for plants
- Implement image annotation

### 2.4 Data Visualization
- Add charts for sensor data
- Add plant growth visualization
- Implement dashboard widgets

## 3. UI/UX Improvements

### 3.1 Styling
- Update CSS to match Isley exactly
- Implement responsive design
- Add proper icons and visual elements

### 3.2 JavaScript Functionality
- Add dynamic form handling
- Implement real-time updates
- Add chart.js integration

## 4. Testing and Refinement

### 4.1 Functionality Testing
- Test all CRUD operations
- Test sensor integration
- Test image uploads
- Test data visualization

### 4.2 UI/UX Testing
- Test responsive design
- Test browser compatibility
- Test mobile usability

## 5. Documentation

### 5.1 User Documentation
- Create user guide
- Add feature documentation
- Include setup instructions

### 5.2 Developer Documentation
- Document code structure
- Add API documentation
- Include extension guidelines
