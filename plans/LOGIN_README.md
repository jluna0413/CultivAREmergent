# CultivAR Login System

## Overview

CultivAR has two login modules:

1. **User Login** - For regular users to access the grow journal
2. **Admin Login** - For administrators to access system settings and diagnostics

Both login modules run on the same port (5000) to avoid confusion.

## User Login

- URL: http://localhost:5000/login
- Default credentials:
  - Username: admin
  - Password: (generated at first run, check console output)

## Admin Login

- URL: http://localhost:5000/admin/login
- Default credentials:
  - Username: admin
  - Password: cultivar_admin

## How to Access

1. Start the application using the `run_consolidated.bat` script
2. Access the user login at http://localhost:5000/login
3. To access the admin login, either:
   - Click the small dot at the bottom of the user login page
   - Go directly to http://localhost:5000/admin/login

## Important Notes

- Do not run multiple instances of CultivAR on different ports
- Always use the `run_consolidated.bat` script to start the application
- The admin login is separate from the user login and has different credentials
- The admin dashboard provides access to system diagnostics and settings

## Troubleshooting

If you encounter issues with the login system:

1. Make sure no other instances of CultivAR are running
2. Check that port 5000 is not in use by another application
3. Clear your browser cache and cookies
4. Restart the application using the `run_consolidated.bat` script
