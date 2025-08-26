# TODO List for CultivAR Audit

This file outlines the remaining steps to complete the audit and testing of the CultivAR application.

## 1. Run the Test Suite

The integration test suite in `backend_test.py` needs to be run to verify the fixes and the overall health of the application.

### Steps:

1.  **Start the application:**
    ```bash
    sudo docker compose -f docker-compose.sqlite.yml up -d --build
    ```
2.  **Modify the test script:**
    The `backend_test.py` script has a hardcoded port of `8001`. The application is running on port `5000`. You will need to change the `base_url` in the script to `http://localhost:5000`.
3.  **Run the tests:**
    ```bash
    python backend_test.py
    ```
4.  **Review the results:**
    The test results will be printed to the console and saved in `backend_test_results.json`.

## 2. Address Vulnerable Dependencies

The `vulnerability_report.md` file contains a list of vulnerable dependencies. These should be updated in `requirements.txt` to their latest stable versions.

## 3. Implement Further Recommendations

The `audit_report.md` file contains a prioritized list of recommendations for improving the codebase. These should be addressed in future development work.

## 4. Manual Verification of XSS Fix

To manually verify the XSS fix:
1.  Create a new user with a malicious email address (e.g., `<script>alert('XSS')</script>`).
2.  Log in as the admin user.
3.  Navigate to the `/admin/users` page.
4.  Verify that the user's email is displayed as plain text and the script is not executed.
