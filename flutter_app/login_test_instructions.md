# Flutter App Login Test Instructions

## App Status
- Flutter app is running on: http://localhost:5050
- Browser opened to login page: http://localhost:5050/login

## Test Credentials
Use these mock credentials for testing:

**Admin Account:**
- Email: admin@cultivar.app
- Password: admin123

**Regular User Account:**
- Email: user@cultivar.app  
- Password: user123

## Manual Test Steps

### 1. Test Admin Login
1. Open Chrome DevTools (F12)
2. Go to the Console tab
3. Clear any existing logs
4. Fill in the login form:
   - Email: `admin@cultivar.app`
   - Password: `admin123`
5. Click the Login button
6. Watch the console for any errors or success messages
7. Check if you get redirected to the dashboard

### 2. Test Regular User Login
1. Clear browser session/storage if needed
2. Fill in the login form:
   - Email: `user@cultivar.app`
   - Password: `user123`
3. Click the Login button
4. Watch console for errors
5. Check if login works properly

### 3. Test Invalid Credentials
1. Try with wrong password (e.g., admin@cultivar.app / wrongpass)
2. Should see proper error handling

## Browser DevTools Analysis

Check these tabs in Chrome DevTools:

### Console Tab
Look for:
- Any JavaScript errors
- Authentication success/failure messages
- Network request failures

### Network Tab
Look for:
- API calls being made
- Response status codes
- Request/response headers

### Application Tab → Local Storage/Session Storage
- Check if authentication tokens are stored
- Verify token format and content

## Expected Behavior
- Admin login should redirect to `/dashboard` 
- User login should redirect to `/dashboard`
- Invalid credentials should show error message
- No "invalid token" errors should appear

## If Issues Persist
Check the browser console for specific error messages and share them for further debugging.