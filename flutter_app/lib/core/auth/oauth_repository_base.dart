import 'package:flutter/foundation.dart';

/// OAuth2 configuration for Keycloak (shared)
class OAuthConfig {
  // Use 10.0.2.2 for Android Emulator, localhost for iOS/Web
  static const String _androidIssuer = 'http://10.0.2.2:8081/realms/cultivar';
  static const String _defaultIssuer = 'http://localhost:8081/realms/cultivar';

  static String get issuer {
    if (kIsWeb) return _defaultIssuer;
    if (defaultTargetPlatform == TargetPlatform.android) return _androidIssuer;
    return _defaultIssuer;
  }

  static const String clientId = 'cultivar-web';

  // Web redirect
  static const String _webRedirectUrl = 'http://localhost:4242/callback';
  // Mobile redirect (Custom Scheme)
  static const String _mobileRedirectUrl = 'com.cultivar.app://login-callback';

  static String get redirectUrl =>
      kIsWeb ? _webRedirectUrl : _mobileRedirectUrl;

  static const String postLogoutRedirectUrl = 'http://localhost:4242/';
  static const List<String> scopes = [
    'openid',
    'profile',
    'email',
    'offline_access',
  ];

  // Keycloak endpoints
  static String get authorizationEndpoint =>
      '$issuer/protocol/openid-connect/auth';
  static String get tokenEndpoint => '$issuer/protocol/openid-connect/token';
  static String get logoutEndpoint => '$issuer/protocol/openid-connect/logout';
  static String get userinfoEndpoint =>
      '$issuer/protocol/openid-connect/userinfo';
}

abstract class OAuthRepository {
  bool get isAuthenticated;
  Map<String, dynamic>? get currentUser;
  String? get accessToken;

  void login();
  Future<bool> handleCallback(String code, String? state);
  Future<void> refreshToken();
  Future<void> logout();
  Future<void> signOut();
  void keycloakLogout();
  Future<Map<String, dynamic>?> getCurrentUser();
  Future<String?> getAccessToken();
  Future<bool> isAccessTokenExpired();
  Future<Map<String, dynamic>?> devLogin(String username, String password);
}
