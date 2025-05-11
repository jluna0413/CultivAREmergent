# CultivAR Admin Login Guide

## Admin Login Credentials

To access the admin dashboard, use the following credentials:

- **Username**: admin
- **Password**: cultivar_admin

## How to Access the Admin Dashboard

1. Go to http://localhost:4200/admin/login directly
   
   OR
   
2. From the user login page (http://localhost:4200/login):
   - Look for a small dot (·) at the bottom of the login form
   - Click on that dot to be taken to the admin login page

## Admin Dashboard Features

The admin dashboard provides access to:

1. **JavaScript Diagnostics** - Enable/disable client-side diagnostics
2. **System Information** - View Python and Flask versions
3. **Error Logs** - View application error logs
4. **Diagnostics Tools** - Test pages and API endpoints

## Troubleshooting

If you encounter issues accessing the admin dashboard:

1. Make sure you're using the correct credentials (admin/cultivar_admin)
2. Clear your browser cache and cookies
3. Restart the application using the run_consolidated.bat script
4. Check that port 4200 is not being used by another application

## Security Note

The admin login is separate from the user login and has different credentials. Keep the admin password secure as it provides access to system diagnostics and settings.
