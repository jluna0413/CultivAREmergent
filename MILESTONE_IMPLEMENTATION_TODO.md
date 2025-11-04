# Milestone Implementation TODO

## Comment 1: Milestone 1 - JWT Authentication Implementation

### FastAPI Backend
- [ ] Examine existing FastAPI structure and dependencies
- [ ] Create `auth.py` router in `app/fastapi_app/routers/` with:
  - `POST /auth/login` endpoint with JWT access+refresh tokens
  - `POST /auth/refresh` endpoint for token refresh
  - `POST /auth/logout` endpoint for token invalidation
- [ ] Implement password hashing and user lookup in `app/models/base_models.py`
- [ ] Wire routers in `app/fastapi_app/__init__.py`
- [ ] Add JWT configuration and dependencies

### Flutter Frontend
- [ ] Implement `AuthService` in `flutter_app/lib/core/services/auth_service.dart`
- [ ] Store tokens in secure storage
- [ ] Update `api_client.dart` with Authorization header interceptor
- [ ] Update `login_screen.dart` to use `AuthService.login()` and route on success
- [ ] Add token refresh and logout flows
- [ ] Test manual login functionality

### Integration & Testing
- [ ] Verify end-to-end JWT flow
- [ ] Test login/logout/refresh scenarios
- [ ] Ensure secure token storage and transmission

## Comment 2: Milestone 2 - Security Hardening

### CORS Configuration
- [ ] Update CORS in `app/fastapi_app/__init__.py` to:
  - Use `FRONTEND_ORIGINS` environment variable
  - Restrict allowed methods appropriately
  - Restrict allowed headers appropriately

### Security Middleware
- [ ] Configure TrustedHost middleware with production domains
- [ ] Create `require_user` dependency reading JWT claims
- [ ] Create `require_admin` dependency reading JWT claims
- [ ] Apply `require_admin` to admin routers

### Documentation
- [ ] Document required environment variables in `README.md`

## Verification Checklist
- [ ] All JWT endpoints working correctly
- [ ] Flutter integration functional
- [ ] CORS properly configured
- [ ] Security dependencies applied
- [ ] Environment variables documented
- [ ] Manual testing completed successfully
