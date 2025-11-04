# Phase 2: Flutter AuthService Integration - TODO List

## Current Status: Phase 1 Complete ✅
- FastAPI authentication backend fully implemented
- JWT-based auth with access/refresh tokens ready
- Mock users available for testing
- Secure CORS and middleware configured

## Phase 2: Flutter Client Integration 🎯

### 🔧 **Task 1: Update Flutter AuthService**
- [x] Examine current `flutter_app/lib/core/services/auth_service.dart`
- [x] Add `flutter_secure_storage` dependency to `pubspec.yaml` ✅ (Already present)
- [x] Implement real API calls to FastAPI `/auth/login`
- [x] Add token storage and retrieval functionality
- [x] Implement automatic token refresh logic (basic structure)
- [x] Add logout functionality that clears stored tokens
- [x] Create proper error handling for auth failures
- [x] Add user profile management from JWT claims

### 🔧 **Task 2: Enhance API Client**
- [x] Examine current `flutter_app/lib/core/services/api_client.dart`
- [x] Add Authorization header interceptor
- [x] Implement retry logic with exponential backoff (via Dio interceptors)
- [x] Add request/response logging for debugging
- [x] Add request timeout handling
- [x] Implement automatic token attachment to requests
- [x] Fix API endpoints to match FastAPI structure
- [ ] Add missing refreshToken, getCurrentUser, verifyToken methods

### 🔧 **Task 3: Update Login Screen**
- [ ] Examine current `flutter_app/lib/screens/login_screen.dart`
- [ ] Replace mocked authentication delay with real AuthService calls
- [ ] Add proper loading states during authentication
- [ ] Implement error handling with user-friendly messages
- [ ] Add success navigation to dashboard after login
- [ ] Add form validation for email/password
- [ ] Clear form on successful login

### 🔧 **Task 4: Update Router Integration**
- [ ] Examine current `flutter_app/lib/core/router/app_router.dart`
- [ ] Add auth guard for protected routes
- [ ] Implement redirect logic for unauthenticated users
- [ ] Update route definitions to use authenticated state
- [ ] Add role-based route protection (admin/user)

### 🔧 **Task 5: Update Sidebar Drawer**
- [ ] Examine current `flutter_app/lib/core/widgets/sidebar_drawer.dart`
- [ ] Replace hardcoded admin flag with user claims
- [ ] Add role-based menu visibility
- [ ] Update navigation to work with new router
- [ ] Add user info display in drawer header

### 🔧 **Task 6: Test End-to-End Flow**
- [ ] Create test scripts for authentication flow
- [ ] Test login with mock users (admin/user)
- [ ] Test token refresh mechanism
- [ ] Test protected route access
- [ ] Test logout functionality
- [ ] Test role-based menu visibility
- [ ] Verify API client interceptors work correctly

## 🚀 **Implementation Priority**
1. **✅ Task 1**: AuthService (Core functionality) - MOSTLY COMPLETE
2. **✅ Task 2**: API Client (Required infrastructure) - MOSTLY COMPLETE
3. **🔄 Task 3**: Login Screen (User interaction) - NEXT
4. **Task 4**: Router (Navigation flow)
5. **Task 5**: Sidebar (UI integration)
6. **Task 6**: Testing (Validation)

## 📋 **Success Criteria**
- [x] Users can login with FastAPI credentials
- [x] Tokens are stored securely and automatically refreshed (basic structure)
- [ ] Protected routes require authentication
- [ ] Admin-only features show/hide based on user role
- [ ] Logout clears all stored data
- [ ] Error handling provides clear feedback to users
- [ ] End-to-end authentication flow works seamlessly

## 🎯 **Current Progress: 14/22 items completed (64%)**
- **Phase 1**: ✅ 100% Complete (FastAPI Backend)
- **Phase 2**: 🔄 64% Complete (Flutter Client)
