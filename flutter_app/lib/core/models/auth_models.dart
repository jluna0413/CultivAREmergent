/// Authentication models for CultivAR mobile app
class User {
  const User({
    required this.id,
    required this.email,
    required this.username,
    this.avatar,
    required this.createdAt,
    required this.updatedAt,
    this.isActive = true,
    this.isAdmin = false,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      email: json['email'] as String,
      username: json['username'] as String,
      avatar: json['avatar'] as String?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      isActive: json['is_active'] as bool? ?? true,
      isAdmin: json['is_admin'] as bool? ?? false,
    );
  }
  final int id;
  final String email;
  final String username;
  final String? avatar;
  final DateTime createdAt;
  final DateTime updatedAt;
  final bool isActive;
  final bool isAdmin;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'username': username,
      'avatar': avatar,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'is_active': isActive,
    };
  }

  User copyWith({
    int? id,
    String? email,
    String? username,
    String? avatar,
    DateTime? createdAt,
    DateTime? updatedAt,
    bool? isActive,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      username: username ?? this.username,
      avatar: avatar ?? this.avatar,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      isActive: isActive ?? this.isActive,
    );
  }
}

class AuthResponse {
  // Add refresh token support

  const AuthResponse({
    required this.accessToken,
    required this.tokenType,
    required this.user,
    this.refreshToken,
  });

  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      accessToken: json['access_token'] as String,
      tokenType: json['token_type'] as String,
      user: User.fromJson(json['user'] as Map<String, dynamic>),
      refreshToken: json['refresh_token'] as String?,
    );
  }
  final String accessToken;
  final String tokenType;
  final User user;
  final String? refreshToken;

  Map<String, dynamic> toJson() {
    return {
      'access_token': accessToken,
      'token_type': tokenType,
      'user': user.toJson(),
      'refresh_token': refreshToken,
    };
  }

  @override
  String toString() {
    return 'AuthResponse{tokenType: $tokenType, user: $user, hasRefreshToken: ${refreshToken != null}}';
  }
}
