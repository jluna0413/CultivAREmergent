// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'admin_user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$AdminUserImpl _$$AdminUserImplFromJson(Map<String, dynamic> json) =>
    _$AdminUserImpl(
      id: (json['id'] as num).toInt(),
      username: json['username'] as String,
      email: json['email'] as String?,
      phone: json['phone'] as String?,
      isAdmin: json['isAdmin'] as bool,
      createdAt: DateTime.parse(json['createdAt'] as String),
      lastLogin: json['lastLogin'] == null
          ? null
          : DateTime.parse(json['lastLogin'] as String),
      isActive: json['isActive'] as bool?,
    );

Map<String, dynamic> _$$AdminUserImplToJson(_$AdminUserImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'username': instance.username,
      'email': instance.email,
      'phone': instance.phone,
      'isAdmin': instance.isAdmin,
      'createdAt': instance.createdAt.toIso8601String(),
      'lastLogin': instance.lastLogin?.toIso8601String(),
      'isActive': instance.isActive,
    };

_$AdminUserCreateImpl _$$AdminUserCreateImplFromJson(
  Map<String, dynamic> json,
) => _$AdminUserCreateImpl(
  username: json['username'] as String,
  password: json['password'] as String,
  email: json['email'] as String?,
  phone: json['phone'] as String?,
  isAdmin: json['isAdmin'] as bool? ?? false,
  forcePasswordChange: json['forcePasswordChange'] as bool? ?? true,
);

Map<String, dynamic> _$$AdminUserCreateImplToJson(
  _$AdminUserCreateImpl instance,
) => <String, dynamic>{
  'username': instance.username,
  'password': instance.password,
  'email': instance.email,
  'phone': instance.phone,
  'isAdmin': instance.isAdmin,
  'forcePasswordChange': instance.forcePasswordChange,
};

_$AdminUserUpdateImpl _$$AdminUserUpdateImplFromJson(
  Map<String, dynamic> json,
) => _$AdminUserUpdateImpl(
  username: json['username'] as String?,
  password: json['password'] as String?,
  email: json['email'] as String?,
  phone: json['phone'] as String?,
  isAdmin: json['isAdmin'] as bool?,
  forcePasswordChange: json['forcePasswordChange'] as bool?,
  isActive: json['isActive'] as bool?,
);

Map<String, dynamic> _$$AdminUserUpdateImplToJson(
  _$AdminUserUpdateImpl instance,
) => <String, dynamic>{
  'username': instance.username,
  'password': instance.password,
  'email': instance.email,
  'phone': instance.phone,
  'isAdmin': instance.isAdmin,
  'forcePasswordChange': instance.forcePasswordChange,
  'isActive': instance.isActive,
};

_$AdminUserListImpl _$$AdminUserListImplFromJson(Map<String, dynamic> json) =>
    _$AdminUserListImpl(
      users: (json['users'] as List<dynamic>)
          .map((e) => AdminUser.fromJson(e as Map<String, dynamic>))
          .toList(),
      total: (json['total'] as num).toInt(),
      page: (json['page'] as num).toInt(),
      pageSize: (json['pageSize'] as num).toInt(),
    );

Map<String, dynamic> _$$AdminUserListImplToJson(_$AdminUserListImpl instance) =>
    <String, dynamic>{
      'users': instance.users,
      'total': instance.total,
      'page': instance.page,
      'pageSize': instance.pageSize,
    };
