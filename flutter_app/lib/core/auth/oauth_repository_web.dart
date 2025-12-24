// OAuth Repository for Keycloak authentication (Web Platform)
// Uses browser redirects for OAuth2 Authorization Code flow

import 'dart:convert';
// ignore: avoid_web_libraries_in_flutter
import 'dart:html' as html;

import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;

import '../constants/app_constants.dart';
import '../api/api_exceptions.dart' as api_ex;
import 'oauth_repository_base.dart'; // Import the abstract interface

/// OAuthRepository handles Keycloak OAuth2 authentication for Web
class OAuthRepositoryWeb implements OAuthRepository {
  // Renamed and implements
  OAuthRepositoryWeb() {
    // Modified constructor
    _storage = const FlutterSecureStorage();
    _init();
  }

  late final FlutterSecureStorage _storage;

  Map<String, dynamic>? _currentUser;
  String? _accessToken;
  String? _refreshToken;
  String? _idToken;

  Future<void> _init() async {
    // Try to restore session from storage
    _accessToken = await _storage.read(key: AppConstants.accessTokenKey);
    _refreshToken = await _storage.read(key: AppConstants.refreshTokenKey);
    _idToken = await _storage.read(key: 'id_token');

    final userJson = await _storage.read(key: 'current_user');
    if (userJson != null) {
      try {
        _currentUser = jsonDecode(userJson) as Map<String, dynamic>;
      } catch (_) {
        _currentUser = null;
      }
    }
  }

  @override
  bool get isAuthenticated => _accessToken != null && _currentUser != null;
  @override
  Map<String, dynamic>? get currentUser => _currentUser;
  @override
  String? get accessToken => _accessToken;

  /// Initiate OAuth2 login flow - redirect to Keycloak
  @override
  void login() {
    // Build authorization URL
    final authUrl = Uri.parse(OAuthConfig.authorizationEndpoint).replace(
      queryParameters: {
        'client_id': OAuthConfig.clientId,
        'response_type': 'code',
        'redirect_uri': OAuthConfig.redirectUrl,
        'scope': OAuthConfig.scopes.join(' '),
        'state': _generateState(),
      },
    );

    // Store state for CSRF protection
    html.window.sessionStorage['oauth_state'] =
        authUrl.queryParameters['state']!;

    // Redirect browser to Keycloak
    html.window.location.href = authUrl.toString();
  }

  /// Generate random state for CSRF protection
  String _generateState() {
    final random = DateTime.now().millisecondsSinceEpoch.toString();
    return base64Url.encode(utf8.encode(random)).substring(0, 16);
  }

  /// Handle OAuth callback - exchange authorization code for tokens
  @override
  Future<bool> handleCallback(String code, String? state) async {
    // Verify state for CSRF protection
    final storedState = html.window.sessionStorage['oauth_state'];
    if (state != null && storedState != state) {
      print('OAuth state mismatch - possible CSRF attack');
      return false;
    }
    html.window.sessionStorage.remove('oauth_state');

    try {
      // Exchange code for tokens
      final response = await http.post(
        Uri.parse(OAuthConfig.tokenEndpoint),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'grant_type': 'authorization_code',
          'client_id': OAuthConfig.clientId,
          'code': code,
          'redirect_uri': OAuthConfig.redirectUrl,
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        await _handleTokenResponse(data);
        return true;
      } else {
        print('Token exchange failed: ${response.statusCode} ${response.body}');
        return false;
      }
    } catch (e) {
      print('Token exchange error: $e');
      return false;
    }
  }

  /// Store tokens and parse user info
  Future<void> _handleTokenResponse(Map<String, dynamic> data) async {
    _accessToken = data['access_token'] as String?;
    _refreshToken = data['refresh_token'] as String?;
    _idToken = data['id_token'] as String?;

    // Store tokens
    if (_accessToken != null) {
      await _storage.write(
        key: AppConstants.accessTokenKey,
        value: _accessToken,
      );
    }
    if (_refreshToken != null) {
      await _storage.write(
        key: AppConstants.refreshTokenKey,
        value: _refreshToken,
      );
    }
    if (_idToken != null) {
      await _storage.write(key: 'id_token', value: _idToken);
    }

    // Parse user info from ID token
    if (_idToken != null) {
      _currentUser = _parseIdToken(_idToken!);
      if (_currentUser != null) {
        await _storage.write(
          key: 'current_user',
          value: jsonEncode(_currentUser),
        );
      }
    }
  }

  /// Parse JWT ID token to extract user info
  Map<String, dynamic>? _parseIdToken(String idToken) {
    try {
      final parts = idToken.split('.');
      if (parts.length != 3) return null;

      final payload = parts[1];
      // Add padding if needed
      final normalized = base64Url.normalize(payload);
      final decoded = utf8.decode(base64Url.decode(normalized));
      return jsonDecode(decoded) as Map<String, dynamic>;
    } catch (e) {
      print('Error parsing ID token: $e');
      return null;
    }
  }

  /// Refresh the access token using the refresh token
  @override
  Future<void> refreshToken() async {
    if (_refreshToken == null) {
      throw api_ex.AuthException(message: 'No refresh token available');
    }

    try {
      final response = await http.post(
        Uri.parse(OAuthConfig.tokenEndpoint),
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: {
          'grant_type': 'refresh_token',
          'client_id': OAuthConfig.clientId,
          'refresh_token': _refreshToken,
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        await _handleTokenResponse(data);
      } else {
        // Clear tokens on refresh failure
        await logout();
        throw api_ex.AuthException(message: 'Token refresh failed');
      }
    } catch (e) {
      await logout();
      throw api_ex.AuthException(message: 'Token refresh failed: $e');
    }
  }

  /// Logout and clear all tokens
  @override
  Future<void> logout() async {
    // Clear local state
    _accessToken = null;
    _refreshToken = null;
    _idToken = null;
    _currentUser = null;

    // Clear storage
    await _storage.delete(key: AppConstants.accessTokenKey);
    await _storage.delete(key: AppConstants.refreshTokenKey);
    await _storage.delete(key: 'id_token');
    await _storage.delete(key: 'current_user');

    // Optionally redirect to Keycloak logout
    // html.window.location.href = '${OAuthConfig.logoutEndpoint}?redirect_uri=${OAuthConfig.postLogoutRedirectUrl}';
  }

  /// Sign out - alias for logout
  @override
  Future<void> signOut() async {
    await logout();
  }

  /// Logout from Keycloak (redirect)
  @override
  void keycloakLogout() {
    html.window.location.href =
        '${OAuthConfig.logoutEndpoint}?redirect_uri=${OAuthConfig.postLogoutRedirectUrl}';
  }

  /// Get current user from stored data
  @override
  Future<Map<String, dynamic>?> getCurrentUser() async {
    if (_currentUser == null) {
      await _init();
    }
    return _currentUser;
  }

  /// Get access token (async version for compatibility)
  @override
  Future<String?> getAccessToken() async {
    if (_accessToken == null) {
      await _init();
    }
    return _accessToken;
  }

  /// Check if access token is expired
  @override
  Future<bool> isAccessTokenExpired() async {
    if (_accessToken == null) return true;

    try {
      final payload = _parseIdToken(_accessToken!);
      if (payload == null) return true;

      final exp = payload['exp'] as int?;
      if (exp == null) return true;

      final expiryDate = DateTime.fromMillisecondsSinceEpoch(exp * 1000);
      return DateTime.now().isAfter(expiryDate);
    } catch (e) {
      return true;
    }
  }

  @override
  Future<Map<String, dynamic>?> devLogin(
    String username,
    String password,
  ) async {
    try {
      // Use localhost:4200 directly for dev login
      final uri = Uri.parse('http://localhost:4200/api/v2/auth/login');
      print('DEBUG devLogin: Attempting login for $username');
      final response = await http.post(
        uri,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'username': username, 'password': password}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;
        print('DEBUG devLogin: Login successful, got response');

        // Store access token directly (FastAPI format, not Keycloak)
        _accessToken = data['access_token'] as String?;
        print(
          'DEBUG devLogin: accessToken = ${_accessToken != null ? "PRESENT (${_accessToken!.length} chars)" : "NULL"}',
        );
        if (_accessToken != null) {
          await _storage.write(
            key: AppConstants.accessTokenKey,
            value: _accessToken,
          );
          print(
            'DEBUG devLogin: Token stored with key ${AppConstants.accessTokenKey}',
          );

          // Verify storage worked
          final verifyToken = await _storage.read(
            key: AppConstants.accessTokenKey,
          );
          print(
            'DEBUG devLogin: Verification read = ${verifyToken != null ? "SUCCESS" : "FAILED"}',
          );
        }

        // Store user from response (FastAPI returns user object directly)
        if (data['user'] != null) {
          _currentUser = data['user'] as Map<String, dynamic>;
          await _storage.write(
            key: 'current_user',
            value: jsonEncode(_currentUser),
          );
          print('DEBUG devLogin: User data stored');
        }

        return data; // Return full response including user data
      } else {
        print('Dev login failed: ${response.statusCode} ${response.body}');
        return null;
      }
    } catch (e) {
      print('Dev login error: $e');
      return null;
    }
  }
}

// Factory constructor for web platforms
OAuthRepository getPlatformOAuthRepository() => OAuthRepositoryWeb();
