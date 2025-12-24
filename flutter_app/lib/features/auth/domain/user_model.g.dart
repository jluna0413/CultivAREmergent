// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$UserImpl _$$UserImplFromJson(Map<String, dynamic> json) => _$UserImpl(
  id: (json['id'] as num?)?.toInt(),
  username: json['username'] as String?,
  email: json['email'] as String?,
  isAdmin: json['isAdmin'] as bool? ?? false,
  forcePasswordChange: json['forcePasswordChange'] as bool? ?? false,
  userType: json['userType'] as String? ?? 'user',
  tier: json['tier'] as String? ?? 'free',
  isVerifiedBreeder: json['isVerifiedBreeder'] as bool? ?? false,
  isActive: json['isActive'] as bool? ?? false,
  phone: json['phone'] as String?,
  createdAt: json['createdAt'] == null
      ? null
      : DateTime.parse(json['createdAt'] as String),
  updatedAt: json['updatedAt'] == null
      ? null
      : DateTime.parse(json['updatedAt'] as String),
);

Map<String, dynamic> _$$UserImplToJson(_$UserImpl instance) =>
    <String, dynamic>{
      'id': instance.id,
      'username': instance.username,
      'email': instance.email,
      'isAdmin': instance.isAdmin,
      'forcePasswordChange': instance.forcePasswordChange,
      'userType': instance.userType,
      'tier': instance.tier,
      'isVerifiedBreeder': instance.isVerifiedBreeder,
      'isActive': instance.isActive,
      'phone': instance.phone,
      'createdAt': instance.createdAt?.toIso8601String(),
      'updatedAt': instance.updatedAt?.toIso8601String(),
    };
