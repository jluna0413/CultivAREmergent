# Keycloak Authentication Migration Specification

## 1. Overview
Migrate the existing custom JWT authentication system to a standard OAuth 2.0 / OpenID Connect (OIDC) flow using Keycloak as the Identity Provider (IdP).

## 2. Architecture
*   **Identity Provider**: Keycloak 23.0 (Running in Docker)
*   **Resource Server**: FastAPI Backend (Validates Access Tokens via JWKS)
*   **Client**: Flutter Application (Public Client, uses PKCE)

## 3. Detailed Requirements

### 3.1 Infrastructure
*   **Docker**: Keycloak service must run on port 8080 (or forwarded).
*   **Network**: Helper services (DB) and Keycloak must share a network with the backend for direct communication if needed (e.g., backchannel logout), though frontend-driven flows are primary.
*   **Realm**: A `cultivar` realm must be configured with:
    *   Client `cultivar-web`: For the Flutter web app.
    *   Client `cultivar-mobile`: For the mobile app (if distinct).
    *   Users: Admin and Standard User.

### 3.2 Backend (FastAPI)
*   **Token Verification**: 
    *   Replace `jose` with `PyJWKClient` (or `python-jose` with JWKS support) to fetch public keys from `http://keycloak:8080/realms/cultivar/protocol/openid-connect/certs`.
    *   Validate `iss` (Issuer) and `aud` (Audience) claims.
*   **User Provisioning**:
    *   Keep "Just-In-Time" (JIT) provisioning in `get_current_user`.
    *   Map Keycloak Roles (`admin`, `user`) to internal User model flags (`is_admin`).
*   **Endpoints**:
    *   **Remove**: `/auth/login` (legacy JWT generation).
    *   **Keep**: `/users/me` (profile info).

### 3.3 Frontend (Flutter)
*   **Library**: Use `flutter_appauth` for OIDC flows.
*   **Flow**: Authorization Code Flow with PKCE.
*   **Storage**: Store Access and Refresh tokens securely (`flutter_secure_storage`).
*   **Interceptors**: Attach Access Token to all API requests automatically.
*   **Refresh**: Handle 401s by attempting to refresh the token using the Refresh Token.

## 4. Configuration
Keycloak configuration to be exported to `keycloak-realm.json` for reproducible builds.
