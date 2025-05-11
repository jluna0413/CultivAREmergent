# CultivAR MVP Test Plan

## Overview

This test plan outlines the testing approach for the CultivAR MVP release. The goal is to ensure that all core functionality is working properly before releasing the application to beta testers.

## Test Environment

- **Browser**: Chrome (latest version)
- **Operating System**: Windows 10/11
- **Screen Resolution**: 1920x1080 (desktop), 375x812 (mobile)

## Test Cases

### 1. Authentication

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| AUTH-01 | User Login | 1. Navigate to login page<br>2. Enter valid credentials<br>3. Click "Sign In" | User is logged in and redirected to dashboard | |
| AUTH-02 | Invalid Login | 1. Navigate to login page<br>2. Enter invalid credentials<br>3. Click "Sign In" | Error message is displayed | |
| AUTH-03 | Logout | 1. Click logout button | User is logged out and redirected to login page | |
| AUTH-04 | Admin Login | 1. Navigate to admin login page<br>2. Enter valid admin credentials<br>3. Click "Sign In" | Admin is logged in and redirected to admin dashboard | |

### 2. Plant Management

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| PLANT-01 | Add Plant | 1. Navigate to Plants page<br>2. Click "Add Plant"<br>3. Fill in required fields<br>4. Click "Save" | Plant is created and appears in the list | |
| PLANT-02 | Edit Plant | 1. Navigate to Plants page<br>2. Click on a plant<br>3. Click "Edit"<br>4. Modify fields<br>5. Click "Save" | Plant is updated with new information | |
| PLANT-03 | Delete Plant | 1. Navigate to Plants page<br>2. Click on a plant<br>3. Click "Delete"<br>4. Confirm deletion | Plant is removed from the list | |
| PLANT-04 | Record Activity | 1. Navigate to plant details<br>2. Click "Add Activity"<br>3. Fill in activity details<br>4. Click "Save" | Activity is recorded and displayed in history | |
| PLANT-05 | Upload Image | 1. Navigate to plant details<br>2. Click "Upload Image"<br>3. Select an image<br>4. Click "Upload" | Image is uploaded and displayed | |

### 3. Strain Management

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| STRAIN-01 | Add Strain | 1. Navigate to Strains page<br>2. Click "Add Strain"<br>3. Fill in required fields<br>4. Click "Save" | Strain is created and appears in the list | |
| STRAIN-02 | Edit Strain | 1. Navigate to Strains page<br>2. Click on a strain<br>3. Click "Edit"<br>4. Modify fields<br>5. Click "Save" | Strain is updated with new information | |
| STRAIN-03 | Delete Strain | 1. Navigate to Strains page<br>2. Click on a strain<br>3. Click "Delete"<br>4. Confirm deletion | Strain is removed from the list | |
| STRAIN-04 | View Strain Details | 1. Navigate to Strains page<br>2. Click on a strain | Strain details are displayed | |

### 4. Dashboard

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| DASH-01 | View Dashboard | 1. Log in<br>2. Navigate to Dashboard | Dashboard displays summary information | |
| DASH-02 | Dashboard Links | 1. Click on various dashboard widgets | User is navigated to the appropriate page | |

### 5. Settings

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| SET-01 | Change Password | 1. Navigate to Settings<br>2. Click "Change Password"<br>3. Enter current and new password<br>4. Click "Save" | Password is updated | |
| SET-02 | Theme Settings | 1. Navigate to Settings<br>2. Toggle theme setting<br>3. Click "Save" | Theme is updated | |
| SET-03 | Configure Zones | 1. Navigate to Settings<br>2. Add/edit zones<br>3. Click "Save" | Zones are updated | |

### 6. Responsive Design

| Test ID | Description | Steps | Expected Result | Status |
|---------|-------------|-------|-----------------|--------|
| RESP-01 | Mobile View | 1. Access application on mobile device<br>2. Navigate through pages | Pages display correctly on mobile | |
| RESP-02 | Tablet View | 1. Access application on tablet<br>2. Navigate through pages | Pages display correctly on tablet | |
| RESP-03 | Desktop View | 1. Access application on desktop<br>2. Navigate through pages | Pages display correctly on desktop | |

## Bug Reporting

For each bug found during testing, record the following information:

1. Test ID
2. Description of the issue
3. Steps to reproduce
4. Expected vs. actual result
5. Screenshots (if applicable)
6. Browser/OS information

## Test Completion Criteria

The MVP is ready for beta testing when:

1. All critical and high-priority test cases pass
2. No blocking bugs remain
3. Core functionality (authentication, plant management, strain management) works as expected
4. The application is usable on desktop and mobile devices