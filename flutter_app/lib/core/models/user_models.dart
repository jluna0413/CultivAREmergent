// Enhanced User model for Cultivar App with role-based access control
// Matches FastAPI User schema with role support

enum UserRole { admin, user, moderator }

enum UserStatus { active, inactive, suspended }

class User {
  const User({
    required this.id,
    required this.username,
    required this.email,
    required this.isActive,
    required this.createdAt,
    this.lastLogin,
    this.updatedAt,
    this.firstName,
    this.lastName,
    this.avatar,
    this.role = UserRole.user,
    this.status = UserStatus.active,
    this.metadata,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      username: json['username'] as String,
      email: json['email'] as String,
      isActive: json['is_active'] as bool? ?? false,
      createdAt: DateTime.parse(json['created_at'] as String),
      lastLogin: json['last_login'] != null
          ? DateTime.parse(json['last_login'] as String)
          : null,
      updatedAt: json['updated_at'] != null
          ? DateTime.parse(json['updated_at'] as String)
          : null,
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      avatar: json['avatar'] as String?,
      role: UserRole.values.firstWhere(
        (r) => r.toString().split('.').last == json['role'],
        orElse: () => UserRole.user,
      ),
      status: UserStatus.values.firstWhere(
        (s) => s.toString().split('.').last == json['status'],
        orElse: () => UserStatus.active,
      ),
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }
  final int id;
  final String username;
  final String email;
  final bool isActive;
  final DateTime createdAt;
  final DateTime? lastLogin;
  final DateTime? updatedAt;
  final String? firstName;
  final String? lastName;
  final String? avatar;
  final UserRole role;
  final UserStatus status;
  final Map<String, dynamic>? metadata;

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'is_active': isActive,
      'created_at': createdAt.toIso8601String(),
      'last_login': lastLogin?.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'first_name': firstName,
      'last_name': lastName,
      'avatar': avatar,
      'role': role.toString().split('.').last,
      'status': status.toString().split('.').last,
      'metadata': metadata,
    };
  }

  String get fullName {
    if (firstName != null && lastName != null) {
      return '$firstName $lastName';
    }
    return username;
  }

  bool get isAuthenticated => isActive && id > 0;

  bool get isAdmin => role == UserRole.admin;

  bool get isModerator => role == UserRole.moderator || isAdmin;

  User copyWith({
    int? id,
    String? username,
    String? email,
    bool? isActive,
    DateTime? createdAt,
    DateTime? lastLogin,
    DateTime? updatedAt,
    String? firstName,
    String? lastName,
    String? avatar,
    UserRole? role,
    UserStatus? status,
    Map<String, dynamic>? metadata,
  }) {
    return User(
      id: id ?? this.id,
      username: username ?? this.username,
      email: email ?? this.email,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
      lastLogin: lastLogin ?? this.lastLogin,
      updatedAt: updatedAt ?? this.updatedAt,
      firstName: firstName ?? this.firstName,
      lastName: lastName ?? this.lastName,
      avatar: avatar ?? this.avatar,
      role: role ?? this.role,
      status: status ?? this.status,
      metadata: metadata ?? this.metadata,
    );
  }

  @override
  String toString() =>
      'User(id: $id, username: $username, email: $email, role: $role)';

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is User && runtimeType == other.runtimeType && id == other.id;

  @override
  int get hashCode => id.hashCode;
}

// User role filter enum
enum UserRoleFilter { all, admin, moderator, user }

// User status filter enum
enum UserStatusFilter { all, active, inactive, suspended }

// User search and pagination
class UserSearchRequest {
  const UserSearchRequest({
    this.search,
    this.roleFilter,
    this.statusFilter,
    this.page = 1,
    this.limit = 20,
    this.sortBy = 'created_at',
    this.sortAscending = false,
  });
  final String? search;
  final UserRoleFilter? roleFilter;
  final UserStatusFilter? statusFilter;
  final int page;
  final int limit;
  final String sortBy;
  final bool sortAscending;

  UserSearchRequest copyWith({
    String? search,
    UserRoleFilter? roleFilter,
    UserStatusFilter? statusFilter,
    int? page,
    int? limit,
    String? sortBy,
    bool? sortAscending,
  }) {
    return UserSearchRequest(
      search: search ?? this.search,
      roleFilter: roleFilter ?? this.roleFilter,
      statusFilter: statusFilter ?? this.statusFilter,
      page: page ?? this.page,
      limit: limit ?? this.limit,
      sortBy: sortBy ?? this.sortBy,
      sortAscending: sortAscending ?? this.sortAscending,
    );
  }
}

// User pagination response
class UserListResponse {
  const UserListResponse({
    required this.users,
    required this.total,
    required this.page,
    required this.limit,
    required this.totalPages,
  });

  factory UserListResponse.fromJson(Map<String, dynamic> json) {
    return UserListResponse(
      users: (json['users'] as List)
          .map((user) => User.fromJson(user as Map<String, dynamic>))
          .toList(),
      total: json['total'] as int,
      page: json['page'] as int,
      limit: json['limit'] as int,
      totalPages: json['total_pages'] as int,
    );
  }
  final List<User> users;
  final int total;
  final int page;
  final int limit;
  final int totalPages;
}

// User registration request
class UserRegistrationRequest {
  const UserRegistrationRequest({
    required this.username,
    required this.email,
    required this.password,
    this.firstName,
    this.lastName,
    this.role = UserRole.user,
  });

  factory UserRegistrationRequest.fromJson(Map<String, dynamic> json) {
    return UserRegistrationRequest(
      username: json['username'] as String,
      email: json['email'] as String,
      password: json['password'] as String,
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      role: UserRole.values.firstWhere(
        (r) => r.toString().split('.').last == json['role'],
        orElse: () => UserRole.user,
      ),
    );
  }
  final String username;
  final String email;
  final String password;
  final String? firstName;
  final String? lastName;
  final UserRole role;

  Map<String, dynamic> toJson() {
    return {
      'username': username,
      'email': email,
      'password': password,
      'first_name': firstName,
      'last_name': lastName,
      'role': role.toString().split('.').last,
    };
  }
}

// User profile update request
class UserProfileUpdateRequest {
  const UserProfileUpdateRequest({
    this.firstName,
    this.lastName,
    this.email,
    this.avatar,
    this.role,
    this.status,
    this.metadata,
  });

  factory UserProfileUpdateRequest.fromJson(Map<String, dynamic> json) {
    return UserProfileUpdateRequest(
      firstName: json['first_name'] as String?,
      lastName: json['last_name'] as String?,
      email: json['email'] as String?,
      avatar: json['avatar'] as String?,
      role: json['role'] != null
          ? UserRole.values.firstWhere(
              (r) => r.toString().split('.').last == json['role'],
              orElse: () => UserRole.user,
            )
          : null,
      status: json['status'] != null
          ? UserStatus.values.firstWhere(
              (s) => s.toString().split('.').last == json['status'],
              orElse: () => UserStatus.active,
            )
          : null,
      metadata: json['metadata'] as Map<String, dynamic>?,
    );
  }
  final String? firstName;
  final String? lastName;
  final String? email;
  final String? avatar;
  final UserRole? role;
  final UserStatus? status;
  final Map<String, dynamic>? metadata;

  Map<String, dynamic> toJson() {
    final json = <String, dynamic>{};
    if (firstName != null) json['first_name'] = firstName;
    if (lastName != null) json['last_name'] = lastName;
    if (email != null) json['email'] = email;
    if (avatar != null) json['avatar'] = avatar;
    if (role != null) json['role'] = role.toString().split('.').last;
    if (status != null) json['status'] = status.toString().split('.').last;
    if (metadata != null) json['metadata'] = metadata;
    return json;
  }
}

// User password change request
class UserPasswordChangeRequest {
  const UserPasswordChangeRequest({
    required this.currentPassword,
    required this.newPassword,
  });

  factory UserPasswordChangeRequest.fromJson(Map<String, dynamic> json) {
    return UserPasswordChangeRequest(
      currentPassword: json['current_password'] as String,
      newPassword: json['new_password'] as String,
    );
  }
  final String currentPassword;
  final String newPassword;

  Map<String, dynamic> toJson() {
    return {'current_password': currentPassword, 'new_password': newPassword};
  }
}

// User analytics data
class UserAnalytics {
  const UserAnalytics({
    required this.totalUsers,
    required this.activeUsers,
    required this.inactiveUsers,
    required this.suspendedUsers,
    required this.adminsCount,
    required this.moderatorsCount,
    required this.regularUsersCount,
    required this.newUsersThisMonth,
    required this.newUsersLastMonth,
    required this.usersByRole,
    required this.usersByStatus,
  });

  factory UserAnalytics.fromJson(Map<String, dynamic> json) {
    return UserAnalytics(
      totalUsers: json['total_users'] as int,
      activeUsers: json['active_users'] as int,
      inactiveUsers: json['inactive_users'] as int,
      suspendedUsers: json['suspended_users'] as int,
      adminsCount: json['admins_count'] as int,
      moderatorsCount: json['moderators_count'] as int,
      regularUsersCount: json['regular_users_count'] as int,
      newUsersThisMonth: json['new_users_this_month'] as int,
      newUsersLastMonth: json['new_users_last_month'] as int,
      usersByRole: Map<String, int>.from(json['users_by_role'] as Map),
      usersByStatus: Map<String, int>.from(json['users_by_status'] as Map),
    );
  }
  final int totalUsers;
  final int activeUsers;
  final int inactiveUsers;
  final int suspendedUsers;
  final int adminsCount;
  final int moderatorsCount;
  final int regularUsersCount;
  final int newUsersThisMonth;
  final int newUsersLastMonth;
  final Map<String, int> usersByRole;
  final Map<String, int> usersByStatus;
}

// Extension for UserRole
extension UserRoleExtension on UserRole {
  String get displayName {
    switch (this) {
      case UserRole.admin:
        return 'Administrator';
      case UserRole.moderator:
        return 'Moderator';
      case UserRole.user:
        return 'User';
      default:
        return 'Unknown';
    }
  }

  String get description {
    switch (this) {
      case UserRole.admin:
        return 'Full access to all features and user management';
      case UserRole.moderator:
        return 'Can moderate content and manage some users';
      case UserRole.user:
        return 'Standard user with basic access';
      default:
        return 'Unknown role';
    }
  }
}

// Extension for UserStatus
extension UserStatusExtension on UserStatus {
  String get displayName {
    switch (this) {
      case UserStatus.active:
        return 'Active';
      case UserStatus.inactive:
        return 'Inactive';
      case UserStatus.suspended:
        return 'Suspended';
      default:
        return 'Unknown';
    }
  }
}
