import 'package:json_annotation/json_annotation.dart';

/// Authentication tokens model for OAuth/JWT token management
class AuthTokens {
  /// Creates AuthTokens with required and optional fields
  const AuthTokens({
    required this.accessToken,
    required this.refreshToken,
    this.expiresIn,
    this.tokenType = 'bearer',
  });

  /// Creates AuthTokens from JSON
  factory AuthTokens.fromJson(Map<String, dynamic> json) {
    return AuthTokens(
      accessToken: json['access_token'] as String,
      refreshToken: json['refresh_token'] as String,
      expiresIn: json['expires_in'] as int?,
      tokenType: json['token_type'] as String? ?? 'bearer',
    );
  }

  /// Access token for API authentication
  @JsonKey(name: 'access_token')
  final String accessToken;

  /// Refresh token for obtaining new access tokens
  @JsonKey(name: 'refresh_token')
  final String refreshToken;

  /// Token expiration time in seconds
  @JsonKey(name: 'expires_in')
  final int? expiresIn;

  /// Token type (default: 'bearer')
  @JsonKey(name: 'token_type')
  final String tokenType;

  /// Converts AuthTokens to JSON
  Map<String, dynamic> toJson() {
    return {
      'access_token': accessToken,
      'refresh_token': refreshToken,
      'expires_in': expiresIn,
      'token_type': tokenType,
    };
  }

  /// Creates a copy with optional field overrides
  AuthTokens copyWith({
    String? accessToken,
    String? refreshToken,
    int? expiresIn,
    String? tokenType,
  }) {
    return AuthTokens(
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
      expiresIn: expiresIn ?? this.expiresIn,
      tokenType: tokenType ?? this.tokenType,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is AuthTokens &&
        other.accessToken == accessToken &&
        other.refreshToken == refreshToken &&
        other.expiresIn == expiresIn &&
        other.tokenType == tokenType;
  }

  @override
  int get hashCode {
    return Object.hash(accessToken, refreshToken, expiresIn, tokenType);
  }

  @override
  String toString() {
    return 'AuthTokens(accessToken: ${accessToken.substring(0, 10)}..., refreshToken: ${refreshToken.substring(0, 10)}..., expiresIn: $expiresIn, tokenType: $tokenType)';
  }
}
