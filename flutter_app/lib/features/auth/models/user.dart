import 'package:json_annotation/json_annotation.dart';

/// User model for authentication and profile management
class User {
  /// Creates User with required and optional fields
  const User({
    required this.id,
    required this.email,
    this.name,
    this.isAdmin = false,
    this.createdAt,
    this.lastLogin,
    this.preferences,
    this.status,
  });

  /// Creates User from JSON
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as String,
      email: json['email'] as String,
      name: json['name'] as String?,
      isAdmin: json['is_admin'] as bool? ?? false,
      createdAt: json['created_at'] == null
          ? null
          : DateTime.parse(json['created_at'] as String),
      lastLogin: json['last_login'] == null
          ? null
          : DateTime.parse(json['last_login'] as String),
      preferences: json['preferences'] as Map<String, dynamic>?,
      status: json['status'] as String?,
    );
  }

  /// Unique user identifier
  @JsonKey(name: 'id')
  final String id;

  /// User email address
  @JsonKey(name: 'email')
  final String email;

  /// User display name
  @JsonKey(name: 'name')
  final String? name;

  /// Admin privileges flag
  @JsonKey(name: 'is_admin')
  final bool isAdmin;

  /// Account creation timestamp
  @JsonKey(name: 'created_at')
  final DateTime? createdAt;

  /// Last login timestamp
  @JsonKey(name: 'last_login')
  final DateTime? lastLogin;

  /// User preferences/settings
  @JsonKey(name: 'preferences')
  final Map<String, dynamic>? preferences;

  /// Account status (active, suspended, etc.)
  @JsonKey(name: 'status')
  final String? status;

  /// Converts User to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'email': email,
      'name': name,
      'is_admin': isAdmin,
      'created_at': createdAt?.toIso8601String(),
      'last_login': lastLogin?.toIso8601String(),
      'preferences': preferences,
      'status': status,
    };
  }

  /// Creates a copy with optional field overrides
  User copyWith({
    String? id,
    String? email,
    String? name,
    bool? isAdmin,
    DateTime? createdAt,
    DateTime? lastLogin,
    Map<String, dynamic>? preferences,
    String? status,
  }) {
    return User(
      id: id ?? this.id,
      email: email ?? this.email,
      name: name ?? this.name,
      isAdmin: isAdmin ?? this.isAdmin,
      createdAt: createdAt ?? this.createdAt,
      lastLogin: lastLogin ?? this.lastLogin,
      preferences: preferences ?? this.preferences,
      status: status ?? this.status,
    );
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is User &&
        other.id == id &&
        other.email == email &&
        other.name == name &&
        other.isAdmin == isAdmin &&
        other.createdAt == createdAt &&
        other.lastLogin == lastLogin &&
        other.preferences == preferences &&
        other.status == status;
  }

  @override
  int get hashCode {
    return Object.hash(
      id,
      email,
      name,
      isAdmin,
      createdAt,
      lastLogin,
      preferences,
      status,
    );
  }

  @override
  String toString() {
    return 'User(id: $id, email: $email, name: $name, isAdmin: $isAdmin, status: $status)';
  }

  /// Convenience getter for user display name
  String get displayName => name ?? email;

  /// Check if user account is active
  bool get isActive => status == 'active' || status == null;

  /// Check if user account is suspended
  bool get isSuspended => status == 'suspended';

  /// Get user role for authorization
  String get role => isAdmin ? 'admin' : 'user';
}
