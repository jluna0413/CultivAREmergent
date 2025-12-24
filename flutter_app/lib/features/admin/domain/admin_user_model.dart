import 'package:freezed_annotation/freezed_annotation.dart';

part 'admin_user_model.freezed.dart';
part 'admin_user_model.g.dart';

/// Admin user model for user management
@freezed
abstract class AdminUser with _$AdminUser {
  const factory AdminUser({
    required int id,
    required String username,
    String? email,
    String? phone,
    required bool isAdmin,
    required DateTime createdAt,
    DateTime? lastLogin,
    bool? isActive,
  }) = _AdminUser;

  factory AdminUser.fromJson(Map<String, dynamic> json) =>
      _$AdminUserFromJson(json);
}

/// Request model for creating new admin users
@freezed
abstract class AdminUserCreate with _$AdminUserCreate {
  const factory AdminUserCreate({
    required String username,
    required String password,
    String? email,
    String? phone,
    @Default(false) bool isAdmin,
    @Default(true) bool forcePasswordChange,
  }) = _AdminUserCreate;

  factory AdminUserCreate.fromJson(Map<String, dynamic> json) =>
      _$AdminUserCreateFromJson(json);
}

/// Request model for updating admin users
@freezed
abstract class AdminUserUpdate with _$AdminUserUpdate {
  const factory AdminUserUpdate({
    String? username,
    String? password,
    String? email,
    String? phone,
    bool? isAdmin,
    bool? forcePasswordChange,
    bool? isActive,
  }) = _AdminUserUpdate;

  factory AdminUserUpdate.fromJson(Map<String, dynamic> json) =>
      _$AdminUserUpdateFromJson(json);
}

/// Response model for admin user list
@freezed
abstract class AdminUserList with _$AdminUserList {
  const factory AdminUserList({
    required List<AdminUser> users,
    required int total,
    required int page,
    required int pageSize,
  }) = _AdminUserList;

  factory AdminUserList.fromJson(Map<String, dynamic> json) =>
      _$AdminUserListFromJson(json);
}
