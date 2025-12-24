// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'admin_user_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
  'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models',
);

AdminUser _$AdminUserFromJson(Map<String, dynamic> json) {
  return _AdminUser.fromJson(json);
}

/// @nodoc
mixin _$AdminUser {
  int get id => throw _privateConstructorUsedError;
  String get username => throw _privateConstructorUsedError;
  String? get email => throw _privateConstructorUsedError;
  String? get phone => throw _privateConstructorUsedError;
  bool get isAdmin => throw _privateConstructorUsedError;
  DateTime get createdAt => throw _privateConstructorUsedError;
  DateTime? get lastLogin => throw _privateConstructorUsedError;
  bool? get isActive => throw _privateConstructorUsedError;

  /// Serializes this AdminUser to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of AdminUser
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AdminUserCopyWith<AdminUser> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminUserCopyWith<$Res> {
  factory $AdminUserCopyWith(AdminUser value, $Res Function(AdminUser) then) =
      _$AdminUserCopyWithImpl<$Res, AdminUser>;
  @useResult
  $Res call({
    int id,
    String username,
    String? email,
    String? phone,
    bool isAdmin,
    DateTime createdAt,
    DateTime? lastLogin,
    bool? isActive,
  });
}

/// @nodoc
class _$AdminUserCopyWithImpl<$Res, $Val extends AdminUser>
    implements $AdminUserCopyWith<$Res> {
  _$AdminUserCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AdminUser
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? username = null,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = null,
    Object? createdAt = null,
    Object? lastLogin = freezed,
    Object? isActive = freezed,
  }) {
    return _then(
      _value.copyWith(
            id: null == id
                ? _value.id
                : id // ignore: cast_nullable_to_non_nullable
                      as int,
            username: null == username
                ? _value.username
                : username // ignore: cast_nullable_to_non_nullable
                      as String,
            email: freezed == email
                ? _value.email
                : email // ignore: cast_nullable_to_non_nullable
                      as String?,
            phone: freezed == phone
                ? _value.phone
                : phone // ignore: cast_nullable_to_non_nullable
                      as String?,
            isAdmin: null == isAdmin
                ? _value.isAdmin
                : isAdmin // ignore: cast_nullable_to_non_nullable
                      as bool,
            createdAt: null == createdAt
                ? _value.createdAt
                : createdAt // ignore: cast_nullable_to_non_nullable
                      as DateTime,
            lastLogin: freezed == lastLogin
                ? _value.lastLogin
                : lastLogin // ignore: cast_nullable_to_non_nullable
                      as DateTime?,
            isActive: freezed == isActive
                ? _value.isActive
                : isActive // ignore: cast_nullable_to_non_nullable
                      as bool?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AdminUserImplCopyWith<$Res>
    implements $AdminUserCopyWith<$Res> {
  factory _$$AdminUserImplCopyWith(
    _$AdminUserImpl value,
    $Res Function(_$AdminUserImpl) then,
  ) = __$$AdminUserImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    int id,
    String username,
    String? email,
    String? phone,
    bool isAdmin,
    DateTime createdAt,
    DateTime? lastLogin,
    bool? isActive,
  });
}

/// @nodoc
class __$$AdminUserImplCopyWithImpl<$Res>
    extends _$AdminUserCopyWithImpl<$Res, _$AdminUserImpl>
    implements _$$AdminUserImplCopyWith<$Res> {
  __$$AdminUserImplCopyWithImpl(
    _$AdminUserImpl _value,
    $Res Function(_$AdminUserImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AdminUser
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? id = null,
    Object? username = null,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = null,
    Object? createdAt = null,
    Object? lastLogin = freezed,
    Object? isActive = freezed,
  }) {
    return _then(
      _$AdminUserImpl(
        id: null == id
            ? _value.id
            : id // ignore: cast_nullable_to_non_nullable
                  as int,
        username: null == username
            ? _value.username
            : username // ignore: cast_nullable_to_non_nullable
                  as String,
        email: freezed == email
            ? _value.email
            : email // ignore: cast_nullable_to_non_nullable
                  as String?,
        phone: freezed == phone
            ? _value.phone
            : phone // ignore: cast_nullable_to_non_nullable
                  as String?,
        isAdmin: null == isAdmin
            ? _value.isAdmin
            : isAdmin // ignore: cast_nullable_to_non_nullable
                  as bool,
        createdAt: null == createdAt
            ? _value.createdAt
            : createdAt // ignore: cast_nullable_to_non_nullable
                  as DateTime,
        lastLogin: freezed == lastLogin
            ? _value.lastLogin
            : lastLogin // ignore: cast_nullable_to_non_nullable
                  as DateTime?,
        isActive: freezed == isActive
            ? _value.isActive
            : isActive // ignore: cast_nullable_to_non_nullable
                  as bool?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminUserImpl implements _AdminUser {
  const _$AdminUserImpl({
    required this.id,
    required this.username,
    this.email,
    this.phone,
    required this.isAdmin,
    required this.createdAt,
    this.lastLogin,
    this.isActive,
  });

  factory _$AdminUserImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminUserImplFromJson(json);

  @override
  final int id;
  @override
  final String username;
  @override
  final String? email;
  @override
  final String? phone;
  @override
  final bool isAdmin;
  @override
  final DateTime createdAt;
  @override
  final DateTime? lastLogin;
  @override
  final bool? isActive;

  @override
  String toString() {
    return 'AdminUser(id: $id, username: $username, email: $email, phone: $phone, isAdmin: $isAdmin, createdAt: $createdAt, lastLogin: $lastLogin, isActive: $isActive)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminUserImpl &&
            (identical(other.id, id) || other.id == id) &&
            (identical(other.username, username) ||
                other.username == username) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.isAdmin, isAdmin) || other.isAdmin == isAdmin) &&
            (identical(other.createdAt, createdAt) ||
                other.createdAt == createdAt) &&
            (identical(other.lastLogin, lastLogin) ||
                other.lastLogin == lastLogin) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    id,
    username,
    email,
    phone,
    isAdmin,
    createdAt,
    lastLogin,
    isActive,
  );

  /// Create a copy of AdminUser
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminUserImplCopyWith<_$AdminUserImpl> get copyWith =>
      __$$AdminUserImplCopyWithImpl<_$AdminUserImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminUserImplToJson(this);
  }
}

abstract class _AdminUser implements AdminUser {
  const factory _AdminUser({
    required final int id,
    required final String username,
    final String? email,
    final String? phone,
    required final bool isAdmin,
    required final DateTime createdAt,
    final DateTime? lastLogin,
    final bool? isActive,
  }) = _$AdminUserImpl;

  factory _AdminUser.fromJson(Map<String, dynamic> json) =
      _$AdminUserImpl.fromJson;

  @override
  int get id;
  @override
  String get username;
  @override
  String? get email;
  @override
  String? get phone;
  @override
  bool get isAdmin;
  @override
  DateTime get createdAt;
  @override
  DateTime? get lastLogin;
  @override
  bool? get isActive;

  /// Create a copy of AdminUser
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AdminUserImplCopyWith<_$AdminUserImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AdminUserCreate _$AdminUserCreateFromJson(Map<String, dynamic> json) {
  return _AdminUserCreate.fromJson(json);
}

/// @nodoc
mixin _$AdminUserCreate {
  String get username => throw _privateConstructorUsedError;
  String get password => throw _privateConstructorUsedError;
  String? get email => throw _privateConstructorUsedError;
  String? get phone => throw _privateConstructorUsedError;
  bool get isAdmin => throw _privateConstructorUsedError;
  bool get forcePasswordChange => throw _privateConstructorUsedError;

  /// Serializes this AdminUserCreate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of AdminUserCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AdminUserCreateCopyWith<AdminUserCreate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminUserCreateCopyWith<$Res> {
  factory $AdminUserCreateCopyWith(
    AdminUserCreate value,
    $Res Function(AdminUserCreate) then,
  ) = _$AdminUserCreateCopyWithImpl<$Res, AdminUserCreate>;
  @useResult
  $Res call({
    String username,
    String password,
    String? email,
    String? phone,
    bool isAdmin,
    bool forcePasswordChange,
  });
}

/// @nodoc
class _$AdminUserCreateCopyWithImpl<$Res, $Val extends AdminUserCreate>
    implements $AdminUserCreateCopyWith<$Res> {
  _$AdminUserCreateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AdminUserCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? username = null,
    Object? password = null,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = null,
    Object? forcePasswordChange = null,
  }) {
    return _then(
      _value.copyWith(
            username: null == username
                ? _value.username
                : username // ignore: cast_nullable_to_non_nullable
                      as String,
            password: null == password
                ? _value.password
                : password // ignore: cast_nullable_to_non_nullable
                      as String,
            email: freezed == email
                ? _value.email
                : email // ignore: cast_nullable_to_non_nullable
                      as String?,
            phone: freezed == phone
                ? _value.phone
                : phone // ignore: cast_nullable_to_non_nullable
                      as String?,
            isAdmin: null == isAdmin
                ? _value.isAdmin
                : isAdmin // ignore: cast_nullable_to_non_nullable
                      as bool,
            forcePasswordChange: null == forcePasswordChange
                ? _value.forcePasswordChange
                : forcePasswordChange // ignore: cast_nullable_to_non_nullable
                      as bool,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AdminUserCreateImplCopyWith<$Res>
    implements $AdminUserCreateCopyWith<$Res> {
  factory _$$AdminUserCreateImplCopyWith(
    _$AdminUserCreateImpl value,
    $Res Function(_$AdminUserCreateImpl) then,
  ) = __$$AdminUserCreateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String username,
    String password,
    String? email,
    String? phone,
    bool isAdmin,
    bool forcePasswordChange,
  });
}

/// @nodoc
class __$$AdminUserCreateImplCopyWithImpl<$Res>
    extends _$AdminUserCreateCopyWithImpl<$Res, _$AdminUserCreateImpl>
    implements _$$AdminUserCreateImplCopyWith<$Res> {
  __$$AdminUserCreateImplCopyWithImpl(
    _$AdminUserCreateImpl _value,
    $Res Function(_$AdminUserCreateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AdminUserCreate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? username = null,
    Object? password = null,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = null,
    Object? forcePasswordChange = null,
  }) {
    return _then(
      _$AdminUserCreateImpl(
        username: null == username
            ? _value.username
            : username // ignore: cast_nullable_to_non_nullable
                  as String,
        password: null == password
            ? _value.password
            : password // ignore: cast_nullable_to_non_nullable
                  as String,
        email: freezed == email
            ? _value.email
            : email // ignore: cast_nullable_to_non_nullable
                  as String?,
        phone: freezed == phone
            ? _value.phone
            : phone // ignore: cast_nullable_to_non_nullable
                  as String?,
        isAdmin: null == isAdmin
            ? _value.isAdmin
            : isAdmin // ignore: cast_nullable_to_non_nullable
                  as bool,
        forcePasswordChange: null == forcePasswordChange
            ? _value.forcePasswordChange
            : forcePasswordChange // ignore: cast_nullable_to_non_nullable
                  as bool,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminUserCreateImpl implements _AdminUserCreate {
  const _$AdminUserCreateImpl({
    required this.username,
    required this.password,
    this.email,
    this.phone,
    this.isAdmin = false,
    this.forcePasswordChange = true,
  });

  factory _$AdminUserCreateImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminUserCreateImplFromJson(json);

  @override
  final String username;
  @override
  final String password;
  @override
  final String? email;
  @override
  final String? phone;
  @override
  @JsonKey()
  final bool isAdmin;
  @override
  @JsonKey()
  final bool forcePasswordChange;

  @override
  String toString() {
    return 'AdminUserCreate(username: $username, password: $password, email: $email, phone: $phone, isAdmin: $isAdmin, forcePasswordChange: $forcePasswordChange)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminUserCreateImpl &&
            (identical(other.username, username) ||
                other.username == username) &&
            (identical(other.password, password) ||
                other.password == password) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.isAdmin, isAdmin) || other.isAdmin == isAdmin) &&
            (identical(other.forcePasswordChange, forcePasswordChange) ||
                other.forcePasswordChange == forcePasswordChange));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    username,
    password,
    email,
    phone,
    isAdmin,
    forcePasswordChange,
  );

  /// Create a copy of AdminUserCreate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminUserCreateImplCopyWith<_$AdminUserCreateImpl> get copyWith =>
      __$$AdminUserCreateImplCopyWithImpl<_$AdminUserCreateImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminUserCreateImplToJson(this);
  }
}

abstract class _AdminUserCreate implements AdminUserCreate {
  const factory _AdminUserCreate({
    required final String username,
    required final String password,
    final String? email,
    final String? phone,
    final bool isAdmin,
    final bool forcePasswordChange,
  }) = _$AdminUserCreateImpl;

  factory _AdminUserCreate.fromJson(Map<String, dynamic> json) =
      _$AdminUserCreateImpl.fromJson;

  @override
  String get username;
  @override
  String get password;
  @override
  String? get email;
  @override
  String? get phone;
  @override
  bool get isAdmin;
  @override
  bool get forcePasswordChange;

  /// Create a copy of AdminUserCreate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AdminUserCreateImplCopyWith<_$AdminUserCreateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AdminUserUpdate _$AdminUserUpdateFromJson(Map<String, dynamic> json) {
  return _AdminUserUpdate.fromJson(json);
}

/// @nodoc
mixin _$AdminUserUpdate {
  String? get username => throw _privateConstructorUsedError;
  String? get password => throw _privateConstructorUsedError;
  String? get email => throw _privateConstructorUsedError;
  String? get phone => throw _privateConstructorUsedError;
  bool? get isAdmin => throw _privateConstructorUsedError;
  bool? get forcePasswordChange => throw _privateConstructorUsedError;
  bool? get isActive => throw _privateConstructorUsedError;

  /// Serializes this AdminUserUpdate to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of AdminUserUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AdminUserUpdateCopyWith<AdminUserUpdate> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminUserUpdateCopyWith<$Res> {
  factory $AdminUserUpdateCopyWith(
    AdminUserUpdate value,
    $Res Function(AdminUserUpdate) then,
  ) = _$AdminUserUpdateCopyWithImpl<$Res, AdminUserUpdate>;
  @useResult
  $Res call({
    String? username,
    String? password,
    String? email,
    String? phone,
    bool? isAdmin,
    bool? forcePasswordChange,
    bool? isActive,
  });
}

/// @nodoc
class _$AdminUserUpdateCopyWithImpl<$Res, $Val extends AdminUserUpdate>
    implements $AdminUserUpdateCopyWith<$Res> {
  _$AdminUserUpdateCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AdminUserUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? username = freezed,
    Object? password = freezed,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = freezed,
    Object? forcePasswordChange = freezed,
    Object? isActive = freezed,
  }) {
    return _then(
      _value.copyWith(
            username: freezed == username
                ? _value.username
                : username // ignore: cast_nullable_to_non_nullable
                      as String?,
            password: freezed == password
                ? _value.password
                : password // ignore: cast_nullable_to_non_nullable
                      as String?,
            email: freezed == email
                ? _value.email
                : email // ignore: cast_nullable_to_non_nullable
                      as String?,
            phone: freezed == phone
                ? _value.phone
                : phone // ignore: cast_nullable_to_non_nullable
                      as String?,
            isAdmin: freezed == isAdmin
                ? _value.isAdmin
                : isAdmin // ignore: cast_nullable_to_non_nullable
                      as bool?,
            forcePasswordChange: freezed == forcePasswordChange
                ? _value.forcePasswordChange
                : forcePasswordChange // ignore: cast_nullable_to_non_nullable
                      as bool?,
            isActive: freezed == isActive
                ? _value.isActive
                : isActive // ignore: cast_nullable_to_non_nullable
                      as bool?,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AdminUserUpdateImplCopyWith<$Res>
    implements $AdminUserUpdateCopyWith<$Res> {
  factory _$$AdminUserUpdateImplCopyWith(
    _$AdminUserUpdateImpl value,
    $Res Function(_$AdminUserUpdateImpl) then,
  ) = __$$AdminUserUpdateImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    String? username,
    String? password,
    String? email,
    String? phone,
    bool? isAdmin,
    bool? forcePasswordChange,
    bool? isActive,
  });
}

/// @nodoc
class __$$AdminUserUpdateImplCopyWithImpl<$Res>
    extends _$AdminUserUpdateCopyWithImpl<$Res, _$AdminUserUpdateImpl>
    implements _$$AdminUserUpdateImplCopyWith<$Res> {
  __$$AdminUserUpdateImplCopyWithImpl(
    _$AdminUserUpdateImpl _value,
    $Res Function(_$AdminUserUpdateImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AdminUserUpdate
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? username = freezed,
    Object? password = freezed,
    Object? email = freezed,
    Object? phone = freezed,
    Object? isAdmin = freezed,
    Object? forcePasswordChange = freezed,
    Object? isActive = freezed,
  }) {
    return _then(
      _$AdminUserUpdateImpl(
        username: freezed == username
            ? _value.username
            : username // ignore: cast_nullable_to_non_nullable
                  as String?,
        password: freezed == password
            ? _value.password
            : password // ignore: cast_nullable_to_non_nullable
                  as String?,
        email: freezed == email
            ? _value.email
            : email // ignore: cast_nullable_to_non_nullable
                  as String?,
        phone: freezed == phone
            ? _value.phone
            : phone // ignore: cast_nullable_to_non_nullable
                  as String?,
        isAdmin: freezed == isAdmin
            ? _value.isAdmin
            : isAdmin // ignore: cast_nullable_to_non_nullable
                  as bool?,
        forcePasswordChange: freezed == forcePasswordChange
            ? _value.forcePasswordChange
            : forcePasswordChange // ignore: cast_nullable_to_non_nullable
                  as bool?,
        isActive: freezed == isActive
            ? _value.isActive
            : isActive // ignore: cast_nullable_to_non_nullable
                  as bool?,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminUserUpdateImpl implements _AdminUserUpdate {
  const _$AdminUserUpdateImpl({
    this.username,
    this.password,
    this.email,
    this.phone,
    this.isAdmin,
    this.forcePasswordChange,
    this.isActive,
  });

  factory _$AdminUserUpdateImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminUserUpdateImplFromJson(json);

  @override
  final String? username;
  @override
  final String? password;
  @override
  final String? email;
  @override
  final String? phone;
  @override
  final bool? isAdmin;
  @override
  final bool? forcePasswordChange;
  @override
  final bool? isActive;

  @override
  String toString() {
    return 'AdminUserUpdate(username: $username, password: $password, email: $email, phone: $phone, isAdmin: $isAdmin, forcePasswordChange: $forcePasswordChange, isActive: $isActive)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminUserUpdateImpl &&
            (identical(other.username, username) ||
                other.username == username) &&
            (identical(other.password, password) ||
                other.password == password) &&
            (identical(other.email, email) || other.email == email) &&
            (identical(other.phone, phone) || other.phone == phone) &&
            (identical(other.isAdmin, isAdmin) || other.isAdmin == isAdmin) &&
            (identical(other.forcePasswordChange, forcePasswordChange) ||
                other.forcePasswordChange == forcePasswordChange) &&
            (identical(other.isActive, isActive) ||
                other.isActive == isActive));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    username,
    password,
    email,
    phone,
    isAdmin,
    forcePasswordChange,
    isActive,
  );

  /// Create a copy of AdminUserUpdate
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminUserUpdateImplCopyWith<_$AdminUserUpdateImpl> get copyWith =>
      __$$AdminUserUpdateImplCopyWithImpl<_$AdminUserUpdateImpl>(
        this,
        _$identity,
      );

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminUserUpdateImplToJson(this);
  }
}

abstract class _AdminUserUpdate implements AdminUserUpdate {
  const factory _AdminUserUpdate({
    final String? username,
    final String? password,
    final String? email,
    final String? phone,
    final bool? isAdmin,
    final bool? forcePasswordChange,
    final bool? isActive,
  }) = _$AdminUserUpdateImpl;

  factory _AdminUserUpdate.fromJson(Map<String, dynamic> json) =
      _$AdminUserUpdateImpl.fromJson;

  @override
  String? get username;
  @override
  String? get password;
  @override
  String? get email;
  @override
  String? get phone;
  @override
  bool? get isAdmin;
  @override
  bool? get forcePasswordChange;
  @override
  bool? get isActive;

  /// Create a copy of AdminUserUpdate
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AdminUserUpdateImplCopyWith<_$AdminUserUpdateImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

AdminUserList _$AdminUserListFromJson(Map<String, dynamic> json) {
  return _AdminUserList.fromJson(json);
}

/// @nodoc
mixin _$AdminUserList {
  List<AdminUser> get users => throw _privateConstructorUsedError;
  int get total => throw _privateConstructorUsedError;
  int get page => throw _privateConstructorUsedError;
  int get pageSize => throw _privateConstructorUsedError;

  /// Serializes this AdminUserList to a JSON map.
  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;

  /// Create a copy of AdminUserList
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  $AdminUserListCopyWith<AdminUserList> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AdminUserListCopyWith<$Res> {
  factory $AdminUserListCopyWith(
    AdminUserList value,
    $Res Function(AdminUserList) then,
  ) = _$AdminUserListCopyWithImpl<$Res, AdminUserList>;
  @useResult
  $Res call({List<AdminUser> users, int total, int page, int pageSize});
}

/// @nodoc
class _$AdminUserListCopyWithImpl<$Res, $Val extends AdminUserList>
    implements $AdminUserListCopyWith<$Res> {
  _$AdminUserListCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  /// Create a copy of AdminUserList
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? users = null,
    Object? total = null,
    Object? page = null,
    Object? pageSize = null,
  }) {
    return _then(
      _value.copyWith(
            users: null == users
                ? _value.users
                : users // ignore: cast_nullable_to_non_nullable
                      as List<AdminUser>,
            total: null == total
                ? _value.total
                : total // ignore: cast_nullable_to_non_nullable
                      as int,
            page: null == page
                ? _value.page
                : page // ignore: cast_nullable_to_non_nullable
                      as int,
            pageSize: null == pageSize
                ? _value.pageSize
                : pageSize // ignore: cast_nullable_to_non_nullable
                      as int,
          )
          as $Val,
    );
  }
}

/// @nodoc
abstract class _$$AdminUserListImplCopyWith<$Res>
    implements $AdminUserListCopyWith<$Res> {
  factory _$$AdminUserListImplCopyWith(
    _$AdminUserListImpl value,
    $Res Function(_$AdminUserListImpl) then,
  ) = __$$AdminUserListImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({List<AdminUser> users, int total, int page, int pageSize});
}

/// @nodoc
class __$$AdminUserListImplCopyWithImpl<$Res>
    extends _$AdminUserListCopyWithImpl<$Res, _$AdminUserListImpl>
    implements _$$AdminUserListImplCopyWith<$Res> {
  __$$AdminUserListImplCopyWithImpl(
    _$AdminUserListImpl _value,
    $Res Function(_$AdminUserListImpl) _then,
  ) : super(_value, _then);

  /// Create a copy of AdminUserList
  /// with the given fields replaced by the non-null parameter values.
  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? users = null,
    Object? total = null,
    Object? page = null,
    Object? pageSize = null,
  }) {
    return _then(
      _$AdminUserListImpl(
        users: null == users
            ? _value._users
            : users // ignore: cast_nullable_to_non_nullable
                  as List<AdminUser>,
        total: null == total
            ? _value.total
            : total // ignore: cast_nullable_to_non_nullable
                  as int,
        page: null == page
            ? _value.page
            : page // ignore: cast_nullable_to_non_nullable
                  as int,
        pageSize: null == pageSize
            ? _value.pageSize
            : pageSize // ignore: cast_nullable_to_non_nullable
                  as int,
      ),
    );
  }
}

/// @nodoc
@JsonSerializable()
class _$AdminUserListImpl implements _AdminUserList {
  const _$AdminUserListImpl({
    required final List<AdminUser> users,
    required this.total,
    required this.page,
    required this.pageSize,
  }) : _users = users;

  factory _$AdminUserListImpl.fromJson(Map<String, dynamic> json) =>
      _$$AdminUserListImplFromJson(json);

  final List<AdminUser> _users;
  @override
  List<AdminUser> get users {
    if (_users is EqualUnmodifiableListView) return _users;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_users);
  }

  @override
  final int total;
  @override
  final int page;
  @override
  final int pageSize;

  @override
  String toString() {
    return 'AdminUserList(users: $users, total: $total, page: $page, pageSize: $pageSize)';
  }

  @override
  bool operator ==(Object other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$AdminUserListImpl &&
            const DeepCollectionEquality().equals(other._users, _users) &&
            (identical(other.total, total) || other.total == total) &&
            (identical(other.page, page) || other.page == page) &&
            (identical(other.pageSize, pageSize) ||
                other.pageSize == pageSize));
  }

  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  int get hashCode => Object.hash(
    runtimeType,
    const DeepCollectionEquality().hash(_users),
    total,
    page,
    pageSize,
  );

  /// Create a copy of AdminUserList
  /// with the given fields replaced by the non-null parameter values.
  @JsonKey(includeFromJson: false, includeToJson: false)
  @override
  @pragma('vm:prefer-inline')
  _$$AdminUserListImplCopyWith<_$AdminUserListImpl> get copyWith =>
      __$$AdminUserListImplCopyWithImpl<_$AdminUserListImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$AdminUserListImplToJson(this);
  }
}

abstract class _AdminUserList implements AdminUserList {
  const factory _AdminUserList({
    required final List<AdminUser> users,
    required final int total,
    required final int page,
    required final int pageSize,
  }) = _$AdminUserListImpl;

  factory _AdminUserList.fromJson(Map<String, dynamic> json) =
      _$AdminUserListImpl.fromJson;

  @override
  List<AdminUser> get users;
  @override
  int get total;
  @override
  int get page;
  @override
  int get pageSize;

  /// Create a copy of AdminUserList
  /// with the given fields replaced by the non-null parameter values.
  @override
  @JsonKey(includeFromJson: false, includeToJson: false)
  _$$AdminUserListImplCopyWith<_$AdminUserListImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
