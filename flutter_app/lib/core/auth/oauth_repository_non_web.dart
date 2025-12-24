// Non-web implementation of OAuthRepository using FlutterAppAuth
import 'dart:convert';
import 'package:flutter_appauth/flutter_appauth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../constants/app_constants.dart';
import 'oauth_repository_base.dart';
import '../api/api_exceptions.dart' as api_ex;

class OAuthRepositoryNonWeb implements OAuthRepository {
  OAuthRepositoryNonWeb() {
    _storage = const FlutterSecureStorage();
    _appAuth = const FlutterAppAuth();
    _init(); // Fire and forget init
  }

  late final FlutterSecureStorage _storage;
  late final FlutterAppAuth _appAuth;

  Map<String, dynamic>? _currentUser;
  String? _accessToken;
  String? _refreshToken;
  String? _idToken;

  Future<void> _init() async {
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
  bool get isAuthenticated => _accessToken != null;

  @override
  Map<String, dynamic>? get currentUser => _currentUser;

  @override
  String? get accessToken => _accessToken;

  @override
  Future<void> login() async {
    try {
      final AuthorizationTokenResponse? result = await _appAuth
          .authorizeAndExchangeCode(
            AuthorizationTokenRequest(
              OAuthConfig.clientId,
              OAuthConfig.redirectUrl,
              issuer: OAuthConfig.issuer,
              scopes: OAuthConfig.scopes,
            ),
          );

      if (result != null) {
        await _handleTokenResponse(result);
      }
    } catch (e) {
      print('OAuth Login error: $e');
      // Rethrow handling might be needed depending on UI
    }
  }

  Future<void> _handleTokenResponse(TokenResponse result) async {
    _accessToken = result.accessToken;
    _refreshToken = result.refreshToken;
    _idToken = result.idToken;

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
      _currentUser = _parseIdToken(_idToken!);
      if (_currentUser != null) {
        await _storage.write(
          key: 'current_user',
          value: jsonEncode(_currentUser),
        );
      }
    }
  }

  Map<String, dynamic>? _parseIdToken(String idToken) {
    try {
      final parts = idToken.split('.');
      if (parts.length != 3) return null;
      final payload = parts[1];
      final normalized = base64Url.normalize(payload);
      final decoded = utf8.decode(base64Url.decode(normalized));
      return jsonDecode(decoded) as Map<String, dynamic>;
    } catch (e) {
      print('Error parsing ID token: $e');
      return null;
    }
  }

  @override
  Future<bool> handleCallback(String code, String? state) async {
    // Not used for AppAuth as it handles the callback internally via intent/custom scheme
    return true;
  }

  @override
  Future<void> refreshToken() async {
    if (_refreshToken == null) {
      throw api_ex.AuthException(message: 'No refresh token available');
    }

    try {
      final TokenResponse? result = await _appAuth.token(
        TokenRequest(
          OAuthConfig.clientId,
          OAuthConfig.redirectUrl,
          issuer: OAuthConfig.issuer,
          refreshToken: _refreshToken,
        ),
      );

      if (result != null) {
        await _handleTokenResponse(result);
      } else {
        await logout();
        throw api_ex.AuthException(message: 'Token refresh failed');
      }
    } catch (e) {
      await logout();
      throw api_ex.AuthException(message: 'Token refresh failed: $e');
    }
  }

  @override
  Future<void> logout() async {
    _accessToken = null;
    _refreshToken = null;
    _idToken = null;
    _currentUser = null;

    await _storage.delete(key: AppConstants.accessTokenKey);
    await _storage.delete(key: AppConstants.refreshTokenKey);
    await _storage.delete(key: 'id_token');
    await _storage.delete(key: 'current_user');
  }

  @override
  Future<void> signOut() async {
    await logout();
    // Verify if we need to call endSession for AppAuth
    /*
    await _appAuth.endSession(EndSessionRequest(
      idTokenHint: _idToken,
      postLogoutRedirectUrl: OAuthConfig.postLogoutRedirectUrl,
      issuer: OAuthConfig.issuer,
    ));
    */
  }

  @override
  void keycloakLogout() {
    // No-op for now, managed by signOut/endSession usually
  }

  @override
  Future<Map<String, dynamic>?> getCurrentUser() async {
    if (_currentUser == null) {
      await _init();
    }
    return _currentUser;
  }

  @override
  Future<String?> getAccessToken() async {
    if (_accessToken == null) {
      await _init();
    }
    // Check expiration and refresh if needed?
    // AppAuth usually manages this or we do it proactively.
    // For now returning simple token.
    return _accessToken;
  }

  @override
  Future<bool> isAccessTokenExpired() async {
    // ... Implement logic similar to Web ...
    return false;
  }

  @override
  Future<Map<String, dynamic>?> devLogin(
    String username,
    String password,
  ) async {
    // Direct login not supported easily with AppAuth without resource owner password grant, used for old dev flow
    throw UnimplementedError('Dev login deprecated in Keycloak flow');
  }
}

OAuthRepository getPlatformOAuthRepository() => OAuthRepositoryNonWeb();
