# Keycloak Migration Plan

## Phase 1: Infrastructure & Configuration
- [ ] **Network Unification**: Update `docker-compose.auth.yml` to use the same network as the main app (`cultivar-network`).
- [ ] **Keycloak Deployment**: Start Keycloak container.
- [ ] **Realm Configuration**:
    - [ ] Create `cultivar` realm.
    - [ ] Create `cultivar-web` client (Public, Redirect URIs: `http://localhost:4242/*`).
    - [ ] Create test users (`admin`, `user`).
    - [ ] Export configuration to `keycloak-realm.json`.

## Phase 2: Backend (FastAPI)
- [ ] **Dependencies**: Add `pyjwt[crypto]` (or verify `python-jose` support for JWKS).
- [ ] **Refactor `jwt_utils.py`**: Implement `verify_token_with_jwks` using Keycloak's certs endpoint.
- [ ] **Update `dependencies.py`**: Switch `get_current_user` to use the new verification.
- [ ] **Deprecate Legacy Auth**: Remove/Disable `/auth/login` endpoint logic (or keep as fallback for tests if strictly needed, but prefer removal).

## Phase 3: Frontend (Flutter)
- [ ] **Service Layer**: Create `services/auth_service.dart` using `flutter_appauth`.
- [ ] **Login UI**: Replace login form with "Login with Keycloak" button (or auto-redirect).
- [ ] **Token Management**: Implement secure storage and auto-refresh logic in `api_client.dart`.

## Phase 4: Verification
- [ ] **Integration Test**: Verify full login flow (Flutter -> Keycloak -> Back to Flutter -> API Call).
- [ ] **Role Check**: Verify `is_admin` flag is correctly set based on Keycloak roles.
