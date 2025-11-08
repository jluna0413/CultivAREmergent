# CultivAR MVP Test Plan

## Overview

This test plan outlines the testing approach for the CultivAR MVP release. The goal is to ensure that all core functionality is working properly before releasing the application to beta testers. This includes both the web frontend and the FastAPI backend.

## Test Environment

- **Web Frontend**:
    - **Browser**: Chrome (latest version)
    - **Operating System**: Windows 10/11
    - **Screen Resolution**: 1920x1080 (desktop), 375x812 (mobile)
- **API Backend**:
    - **Tool**: Postman, Swagger UI (`/docs`), or custom Python scripts
    - **Target**: Staging or local development server

## Test Cases - Web Frontend

### 1. Authentication

| Test ID | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|-------------|-------|-----------------|---------------------|--------|
| WEB-AUTH-01 | User Login | 1. Navigate to login page<br>2. Enter valid credentials<br>3. Click "Sign In" | User is logged in and redirected to dashboard | User can log in with correct credentials. | |
| WEB-AUTH-02 | Invalid Login | 1. Navigate to login page<br>2. Enter invalid credentials<br>3. Click "Sign In" | Error message is displayed | User cannot log in with incorrect credentials. | |
| WEB-AUTH-03 | Logout | 1. Click logout button | User is logged out and redirected to login page | User can log out successfully. | |

### 2. Plant Management

| Test ID | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|-------------|-------|-----------------|---------------------|--------|
| WEB-PLANT-01 | View Plants | 1. Navigate to Plants page | List of plants is displayed correctly | User can view a list of their plants. | |
| WEB-PLANT-02 | Add Plant | 1. Click "Add Plant"<br>2. Fill in form<br>3. Click "Save" | New plant appears in the list | User can add a new plant. | |
| WEB-PLANT-03 | Edit Plant | 1. Select a plant<br>2. Click "Edit"<br>3. Modify form<br>4. Click "Save" | Plant details are updated | User can edit an existing plant. | |

## Test Cases - API Backend

### 1. Authentication (`/api/v1/auth`)

| Test ID | Endpoint | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|----------|-------------|-------|-----------------|---------------------|--------|
| API-AUTH-01 | `POST /token` | Successful login | 1. Send valid username and password | 200 OK with access and refresh tokens | A valid user can authenticate and receive tokens. | |
| API-AUTH-02 | `POST /token` | Failed login | 1. Send invalid credentials | 401 Unauthorized | An invalid user cannot authenticate. | |
| API-AUTH-03 | `POST /register` | Successful registration | 1. Send unique username and email | 201 Created with user details | A new user can register an account. | |
| API-AUTH-04 | `POST /register` | Duplicate username | 1. Send existing username | 409 Conflict | A user cannot register with an existing username. | |
| API-AUTH-05 | `GET /me` | Get current user | 1. Send request with valid token | 200 OK with current user's details | An authenticated user can retrieve their own profile. | |

### 2. Plants (`/api/v1/plants`)

| Test ID | Endpoint | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|----------|-------------|-------|-----------------|---------------------|--------|
| API-PLANT-01 | `GET /` | List plants | 1. Send request with valid token | 200 OK with a paginated list of plants | A user can retrieve a list of their plants. | |
| API-PLANT-02 | `POST /` | Create plant | 1. Send valid plant data and token | 201 Created with the new plant's details | A user can create a new plant. | |
| API-PLANT-03 | `GET /{plant_id}` | Get single plant | 1. Send request for an existing plant ID | 200 OK with the plant's details | A user can retrieve a single plant by ID. | |
| API-PLANT-04 | `PUT /{plant_id}` | Update plant | 1. Send valid update data for a plant | 200 OK with the updated plant's details | A user can update an existing plant. | |
| API-PLANT-05 | `DELETE /{plant_id}` | Delete plant | 1. Send request to delete an existing plant | 204 No Content | A user can delete a plant. | |

### 3. Cultivars (`/api/v1/cultivars`)

| Test ID | Endpoint | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|----------|-------------|-------|-----------------|---------------------|--------|
| API-CULTIVAR-01 | `GET /` | List cultivars | 1. Send request with valid token | 200 OK with a paginated list of cultivars | A user can retrieve a list of cultivars. | |
| API-CULTIVAR-02 | `POST /` | Create cultivar | 1. Send valid cultivar data and token | 201 Created with the new cultivar's details | A user can create a new cultivar. | |

### 4. Admin (`/api/v1/admin`)

| Test ID | Endpoint | Description | Steps | Expected Result | Acceptance Criteria | Status |
|---------|----------|-------------|-------|-----------------|---------------------|--------|
| API-ADMIN-01 | `GET /users` | List users (as admin) | 1. Send request with admin token | 200 OK with a list of all users | An admin can retrieve a list of all users. | |
| API-ADMIN-02 | `GET /users` | List users (as non-admin) | 1. Send request with regular user token | 403 Forbidden | A non-admin user cannot retrieve a list of all users. | |
| API-ADMIN-03 | `POST /users/bulk-delete` | Bulk delete users | 1. Send list of user IDs to delete | 200 OK with success message | An admin can bulk delete users. | |

## Bug Reporting

For each bug found during testing, record the following information:

1. Test ID
2. Description of the issue
3. Steps to reproduce
4. Expected vs. actual result
5. Screenshots or API response snippets
6. Browser/OS information for frontend bugs

## Test Completion Criteria

The MVP is ready for beta testing when:

1. All critical and high-priority test cases pass for both frontend and backend.
2. No blocking bugs remain in core features.
3. Core functionality (authentication, plant management, cultivar management) works as expected via the API.
4. The web application is usable on desktop and mobile devices.