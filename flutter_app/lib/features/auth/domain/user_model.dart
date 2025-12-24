import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_model.freezed.dart';
part 'user_model.g.dart';

@freezed
abstract class User with _$User {
  const User._();

  const factory User({
    int? id,
    String? username,
    String? email,
    @Default(false) bool isAdmin,
    @Default(false) bool forcePasswordChange,
    @Default('user') String userType,
    @Default('free') String tier,
    @Default(false) bool isVerifiedBreeder,
    @Default(false) bool isActive,
    String? phone,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);

  bool get isAdminRole => isAdmin;
  bool get isVerifiedBreederRole => isVerifiedBreeder;

  String get displayName => username ?? email ?? 'User';
}
