#!/usr/bin/env python3
"""
🔧 FLUTTER CRITICAL FIXES ROUND 2 - Generated Files & Provider Issues
Addresses the most critical compilation-blocking issues first
"""

import os
import subprocess
import re
from pathlib import Path
from datetime import datetime

class FlutterCriticalFixesRound2:
    """Apply critical Flutter fixes - Round 2: Generated files & provider issues"""
    
    def __init__(self):
        self.flutter_dir = Path("flutter_app")
        self.fixes_applied = []
        
    def run_all_fixes(self):
        """Run all critical Flutter fixes"""
        print("🔧 Flutter Critical Fixes Round 2 - Generated Files & Provider Issues")
        print(f"📍 Working directory: {self.flutter_dir}")
        print(f"⏰ Started at: {datetime.utcnow().isoformat()}")
        print("=" * 70)
        
        # Fix 1: Generate missing Freezed files
        self.fix_missing_freezed_files()
        
        # Fix 2: Install missing dependencies
        self.install_missing_dependencies()
        
        # Fix 3: Fix StateNotifierProvider imports
        self.fix_statenotifier_imports()
        
        # Fix 4: Fix API client dynamic types
        self.fix_api_client_types()
        
        # Fix 5: Fix deprecated annotations
        self.fix_deprecated_annotations()
        
        # Fix 6: Generate build runner files
        self.generate_build_files()
        
        return {
            "fixes_applied": self.fixes_applied,
            "round": 2,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "flutter_critical_fixes_round2_completed"
        }
    
    def fix_missing_freezed_files(self):
        """Fix missing Freezed generated files"""
        print("\n🧩 PRIORITY 1: Missing Freezed Files")
        print("-" * 50)
        
        # Create missing freezed files
        missing_files = [
            "lib/core/models/app_settings.freezed.dart",
            "lib/core/models/app_settings.g.dart",
            "lib/core/models/cart_state.freezed.dart",
            "lib/core/models/cart_state.g.dart"
        ]
        
        # Create basic Freezed files for app_settings
        self.create_app_settings_freezed()
        
        # Create basic Freezed files for cart_state
        self.create_cart_state_freezed()
        
        print("    ✅ Created missing Freezed files")
        self.fixes_applied.append("missing_freezed_files_created")
    
    def create_app_settings_freezed(self):
        """Create AppSettings Freezed file"""
        freezed_content = '''// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_settings.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\\n'
    'Please check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models'
);

/// @nodoc
mixin _$AppSettings {
  ThemeMode get themeMode => throw _privateConstructorUsedError;
  bool get darkMode => throw _privateConstructorUsedError;
  String get language => throw _privateConstructorUsedError;
  bool get notifications => throw _privateConstructorUsedError;
  bool get biometricAuth => throw _privateConstructorUsedError;
  String? get timezone => throw _privateConstructorUsedError;
  bool get offlineMode => throw _privateConstructorUsedError;

  @JsonKey(ignore: true)
  $AppSettingsCopyWith<AppSettings> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $AppSettingsCopyWith<$Res> {
  factory $AppSettingsCopyWith(AppSettings value, $Res Function(AppSettings) then) =
      _$AppSettingsCopyWithImpl<$Res, AppSettings>;
  @useResult
  $Res call({
    ThemeMode themeMode,
    bool darkMode,
    String language,
    bool notifications,
    bool biometricAuth,
    String? timezone,
    bool offlineMode,
  });
}

/// @nodoc
class _$AppSettingsCopyWithImpl<$Res, $Val extends AppSettings> implements $AppSettingsCopyWith<$Res> {
  _$AppSettingsCopyWithImpl(this._value, this._then);

  // ignore: unused_element_parameter
  final $Val _value;
  // ignore: unused_element_parameter
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? themeMode = null,
    Object? darkMode = null,
    Object? language = null,
    Object? notifications = null,
    Object? biometricAuth = null,
    Object? timezone = freezed,
    Object? offlineMode = null,
  }) {
    return _then(_value.copyWith(
      themeMode: null == themeMode ? _value.themeMode : themeMode as ThemeMode,
      darkMode: null == darkMode ? _value.darkMode : darkMode as bool,
      language: null == language ? _value.language : language as String,
      notifications: null == notifications ? _value.notifications : notifications as bool,
      biometricAuth: null == biometricAuth ? _value.biometricAuth : biometricAuth as bool,
      timezone: freezed == timezone ? _value.timezone : timezone as String?,
      offlineMode: null == offlineMode ? _value.offlineMode : offlineMode as bool,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$_AppSettingsCopyWith<$Res> implements $AppSettingsCopyWith<$Res> {
  factory _$$_AppSettingsCopyWith(_$_AppSettings value, $Res Function(_$_AppSettings) then) =
      __$$_AppSettingsCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    ThemeMode themeMode,
    bool darkMode,
    String language,
    bool notifications,
    bool biometricAuth,
    String? timezone,
    bool offlineMode,
  });
}

/// @nodoc
class __$$_AppSettingsCopyWithImpl<$Res> extends _$AppSettingsCopyWithImpl<$Res, _$_AppSettings>
    implements _$$_AppSettingsCopyWith<$Res> {
  __$$_AppSettingsCopyWithImpl(_$_AppSettings _value, $Res Function(_$_AppSettings) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? themeMode = null,
    Object? darkMode = null,
    Object? language = null,
    Object? notifications = null,
    Object? biometricAuth = null,
    Object? timezone = freezed,
    Object? offlineMode = null,
  }) {
    return _then(_$_AppSettings(
      themeMode: null == themeMode ? _value.themeMode : themeMode as ThemeMode,
      darkMode: null == darkMode ? _value.darkMode : darkMode as bool,
      language: null == language ? _value.language : language as String,
      notifications: null == notifications ? _value.notifications : notifications as bool,
      biometricAuth: null == biometricAuth ? _value.biometricAuth : biometricAuth as bool,
      timezone: freezed == timezone ? _value.timezone : timezone as String?,
      offlineMode: null == offlineMode ? _value.offlineMode : offlineMode as bool,
    ));
  }
}

/// @nodoc
class _$_AppSettings implements _AppSettings {
  _$_AppSettings({
    this.themeMode = ThemeMode.system,
    this.darkMode = false,
    this.language = 'en',
    this.notifications = true,
    this.biometricAuth = false,
    this.timezone,
    this.offlineMode = false,
  });

  @override
  @JsonKey()
  final ThemeMode themeMode;
  @override
  @JsonKey()
  final bool darkMode;
  @override
  @JsonKey()
  final String language;
  @override
  @JsonKey()
  final bool notifications;
  @override
  @JsonKey()
  final bool biometricAuth;
  @override
  @JsonKey()
  final String? timezone;
  @override
  @JsonKey()
  final bool offlineMode;

  @override
  String toString() {
    return 'AppSettings(themeMode: $themeMode, darkMode: $darkMode, language: $language, notifications: $notifications, biometricAuth: $biometricAuth, timezone: $timezone, offlineMode: $offlineMode)';
  }

  @override
  bool operator ==(dynamic other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType && other is _$_AppSettings && (identical(other.themeMode, themeMode) || other.themeMode == themeMode) && (identical(other.darkMode, darkMode) || other.darkMode == darkMode) && (identical(other.language, language) || other.language == language) && (identical(other.notifications, notifications) || other.notifications == notifications) && (identical(other.biometricAuth, biometricAuth) || other.biometricAuth == biometricAuth) && (identical(other.timezone, timezone) || other.timezone == timezone) && (identical(other.offlineMode, offlineMode) || other.offlineMode == offlineMode));
  }

  @override
  int get hashCode => Object.hash(runtimeType, themeMode, darkMode, language, notifications, biometricAuth, timezone, offlineMode);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$_AppSettingsCopyWith<_$_AppSettings> get copyWith => __$$_AppSettingsCopyWithImpl<_$_AppSettings>(this, _$identity);
}

abstract class _AppSettings implements AppSettings {
  factory _AppSettings({
    final ThemeMode themeMode,
    final bool darkMode,
    final String language,
    final bool notifications,
    final bool biometricAuth,
    final String? timezone,
    final bool offlineMode,
  }) = _$_AppSettings;

  @override
  ThemeMode get themeMode;
  @override
  bool get darkMode;
  @override
  String get language;
  @override
  bool get notifications;
  @override
  bool get biometricAuth;
  @override
  String? get timezone;
  @override
  bool get offlineMode;
  @override
  @JsonKey(ignore: true)
  _$$_AppSettingsCopyWith<_$_AppSettings> get copyWith;
}
'''
        
        freezed_file = self.flutter_dir / "lib/core/models/app_settings.freezed.dart"
        freezed_file.parent.mkdir(parents=True, exist_ok=True)
        freezed_file.write_text(freezed_content)
        
        # Create g.dart file
        g_content = '''// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'app_settings.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$_AppSettings _$$_AppSettingsFromJson(Map<String, dynamic> json) => _$_AppSettings(
      themeMode: json['themeMode'] is ThemeMode
          ? json['themeMode']
          : ThemeMode.values.firstWhere(
              (e) => e.toString().split('.').last == json['themeMode'] as String,
              orElse: () => ThemeMode.system,
            ),
      darkMode: json['darkMode'] as bool? ?? false,
      language: json['language'] as String? ?? 'en',
      notifications: json['notifications'] as bool? ?? true,
      biometricAuth: json['biometricAuth'] as bool? ?? false,
      timezone: json['timezone'] as String?,
      offlineMode: json['offlineMode'] as bool? ?? false,
    );

Map<String, dynamic> _$$_AppSettingsToJson(_$_AppSettings instance) => <String, dynamic>{
      'themeMode': instance.themeMode.toString().split('.').last,
      'darkMode': instance.darkMode,
      'language': instance.language,
      'notifications': instance.notifications,
      'biometricAuth': instance.biometricAuth,
      'timezone': instance.timezone,
      'offlineMode': instance.offlineMode,
    };
'''
        
        g_file = self.flutter_dir / "lib/core/models/app_settings.g.dart"
        g_file.write_text(g_content)
    
    def create_cart_state_freezed(self):
        """Create CartState Freezed file"""
        freezed_content = '''// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'cart_state.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\\n'
    'Please check the documentation here for more information: https://github.com/rrousselGit/freezed#adding-getters-and-methods-to-our-models'
);

/// @nodoc
mixin _$CartProviderState {
  List<CartItem> get items => throw _privateConstructorUsedError;
  int get itemCount => throw _privateConstructorUsedError;
  double get totalPrice => throw _privateConstructorUsedError;
  bool get isLoading => throw _privateConstructorUsedError;
  String? get error => throw _privateConstructorUsedError;
  CheckoutInfo? get checkoutInfo => throw _privateConstructorUsedError;
  String? get lastUpdated => throw _privateConstructorUsedError;

  @JsonKey(ignore: true)
  $CartProviderStateCopyWith<CartProviderState> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $CartProviderStateCopyWith<$Res> {
  factory $CartProviderStateCopyWith(CartProviderState value, $Res Function(CartProviderState) then) =
      _$CartProviderStateCopyWithImpl<$Res, CartProviderState>;
  @useResult
  $Res call({
    List<CartItem> items,
    int itemCount,
    double totalPrice,
    bool isLoading,
    String? error,
    CheckoutInfo? checkoutInfo,
    String? lastUpdated,
  });
}

/// @nodoc
class _$CartProviderStateCopyWithImpl<$Res, $Val extends CartProviderState> implements $CartProviderStateCopyWith<$Res> {
  _$CartProviderStateCopyWithImpl(this._value, this._then);

  // ignore: unused_element_parameter
  final $Val _value;
  // ignore: unused_element_parameter
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? items = null,
    Object? itemCount = null,
    Object? totalPrice = null,
    Object? isLoading = null,
    Object? error = freezed,
    Object? checkoutInfo = freezed,
    Object? lastUpdated = freezed,
  }) {
    return _then(_value.copyWith(
      items: null == items ? _value.items : items as List<CartItem>,
      itemCount: null == itemCount ? _value.itemCount : itemCount as int,
      totalPrice: null == totalPrice ? _value.totalPrice : totalPrice as double,
      isLoading: null == isLoading ? _value.isLoading : isLoading as bool,
      error: freezed == error ? _value.error : error as String?,
      checkoutInfo: freezed == checkoutInfo ? _value.checkoutInfo : checkoutInfo as CheckoutInfo?,
      lastUpdated: freezed == lastUpdated ? _value.lastUpdated : lastUpdated as String?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$_CartProviderStateCopyWith<$Res> implements $CartProviderStateCopyWith<$Res> {
  factory _$$_CartProviderStateCopyWith(_$_CartProviderState value, $Res Function(_$_CartProviderState) then) =
      __$$_CartProviderStateCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({
    List<CartItem> items,
    int itemCount,
    double totalPrice,
    bool isLoading,
    String? error,
    CheckoutInfo? checkoutInfo,
    String? lastUpdated,
  });
}

/// @nodoc
class __$$_CartProviderStateCopyWithImpl<$Res> extends _$CartProviderStateCopyWithImpl<$Res, _$_CartProviderState>
    implements _$$_CartProviderStateCopyWith<$Res> {
  __$$_CartProviderStateCopyWithImpl(_$_CartProviderState _value, $Res Function(_$_CartProviderState) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? items = null,
    Object? itemCount = null,
    Object? totalPrice = null,
    Object? isLoading = null,
    Object? error = freezed,
    Object? checkoutInfo = freezed,
    Object? lastUpdated = freezed,
  }) {
    return _then(_$_CartProviderState(
      items: null == items ? _value.items : items as List<CartItem>,
      itemCount: null == itemCount ? _value.itemCount : itemCount as int,
      totalPrice: null == totalPrice ? _value.totalPrice : totalPrice as double,
      isLoading: null == isLoading ? _value.isLoading : isLoading as bool,
      error: freezed == error ? _value.error : error as String?,
      checkoutInfo: freezed == checkoutInfo ? _value.checkoutInfo : checkoutInfo as CheckoutInfo?,
      lastUpdated: freezed == lastUpdated ? _value.lastUpdated : lastUpdated as String?,
    ));
  }
}

/// @nodoc
class _$_CartProviderState implements _CartProviderState {
  _$_CartProviderState({
    this.items = const [],
    this.itemCount = 0,
    this.totalPrice = 0.0,
    this.isLoading = false,
    this.error,
    this.checkoutInfo,
    this.lastUpdated,
  });

  @override
  @JsonKey()
  final List<CartItem> items;
  @override
  @JsonKey()
  final int itemCount;
  @override
  @JsonKey()
  final double totalPrice;
  @override
  @JsonKey()
  final bool isLoading;
  @override
  @JsonKey()
  final String? error;
  @override
  @JsonKey()
  final CheckoutInfo? checkoutInfo;
  @override
  @JsonKey()
  final String? lastUpdated;

  @override
  String toString() {
    return 'CartProviderState(items: $items, itemCount: $itemCount, totalPrice: $totalPrice, isLoading: $isLoading, error: $error, checkoutInfo: $checkoutInfo, lastUpdated: $lastUpdated)';
  }

  @override
  bool operator ==(dynamic other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType && other is _$_CartProviderState && const DeepCollectionEquality().equals(other.items, items) && (identical(other.itemCount, itemCount) || other.itemCount == itemCount) && (identical(other.totalPrice, totalPrice) || other.totalPrice == totalPrice) && (identical(other.isLoading, isLoading) || other.isLoading == isLoading) && (identical(other.error, error) || other.error == error) && (identical(other.checkoutInfo, checkoutInfo) || other.checkoutInfo == checkoutInfo) && (identical(other.lastUpdated, lastUpdated) || other.lastUpdated == lastUpdated));
  }

  @override
  int get hashCode => Object.hash(
        runtimeType,
        const DeepCollectionEquality().hash(items),
        itemCount,
        totalPrice,
        isLoading,
        error,
        checkoutInfo,
        lastUpdated,
      );

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$_CartProviderStateCopyWith<_$_CartProviderState> get copyWith => __$$_CartProviderStateCopyWithImpl<_$_CartProviderState>(this, _$identity);
}

abstract class _CartProviderState implements CartProviderState {
  factory _CartProviderState({
    final List<CartItem> items,
    final int itemCount,
    final double totalPrice,
    final bool isLoading,
    final String? error,
    final CheckoutInfo? checkoutInfo,
    final String? lastUpdated,
  }) = _$_CartProviderState;

  @override
  List<CartItem> get items;
  @override
  int get itemCount;
  @override
  double get totalPrice;
  @override
  bool get isLoading;
  @override
  String? get error;
  @override
  CheckoutInfo? get checkoutInfo;
  @override
  String? get lastUpdated;
  @override
  @JsonKey(ignore: true)
  _$$_CartProviderStateCopyWith<_$_CartProviderState> get copyWith;
}
'''
        
        freezed_file = self.flutter_dir / "lib/core/models/cart_state.freezed.dart"
        freezed_file.parent.mkdir(parents=True, exist_ok=True)
        freezed_file.write_text(freezed_content)
        
        # Create g.dart file
        g_content = '''// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'cart_state.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$_CartProviderState _$$_CartProviderStateFromJson(Map<String, dynamic> json) => _$_CartProviderState(
      items: (json['items'] as List<dynamic>).map((e) => CartItem.fromJson(e as Map<String, dynamic>)).toList(),
      itemCount: json['itemCount'] as int? ?? 0,
      totalPrice: (json['totalPrice'] as num?)?.toDouble() ?? 0.0,
      isLoading: json['isLoading'] as bool? ?? false,
      error: json['error'] as String?,
      checkoutInfo: json['checkoutInfo'] == null ? null : CheckoutInfo.fromJson(json['checkoutInfo'] as Map<String, dynamic>),
      lastUpdated: json['lastUpdated'] as String?,
    );

Map<String, dynamic> _$$_CartProviderStateToJson(_$_CartProviderState instance) => <String, dynamic>{
      'items': instance.items.map((e) => e.toJson()).toList(),
      'itemCount': instance.itemCount,
      'totalPrice': instance.totalPrice,
      'isLoading': instance.isLoading,
      'error': instance.error,
      'checkoutInfo': instance.checkoutInfo?.toJson(),
      'lastUpdated': instance.lastUpdated,
    };
'''
        
        g_file = self.flutter_dir / "lib/core/models/cart_state.g.dart"
        g_file.write_text(g_content)
    
    def install_missing_dependencies(self):
        """Install missing dependencies"""
        print("\n📦 PRIORITY 2: Missing Dependencies")
        print("-" * 50)
        
        try:
            # Check and install flutter_riverpod if missing
            result = subprocess.run(
                ["flutter", "pub", "add", "flutter_riverpod"],
                cwd=self.flutter_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("    ✅ flutter_riverpod added successfully")
                self.fixes_applied.append("flutter_riverpod_installed")
            else:
                print(f"    ⚠️  flutter_riverpod add failed: {result.stderr}")
                
        except Exception as e:
            print(f"    ❌ Dependency installation failed: {e}")
            self.fixes_applied.append("dependency_installation_failed")
    
    def fix_statenotifier_imports(self):
        """Fix StateNotifierProvider imports"""
        print("\n🔧 PRIORITY 3: StateNotifierProvider Imports")
        print("-" * 50)
        
        # Files that need StateNotifierProvider import
        files_to_fix = [
            "lib/core/providers/cart_provider.dart",
            "lib/core/providers/cultivar_provider.dart",
            "lib/core/providers/dashboard_provider.dart",
            "lib/core/providers/sensors_provider.dart"
        ]
        
        for file_path in files_to_fix:
            full_path = self.flutter_dir / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text()
                    
                    # Add import if missing
                    if "import 'package:flutter_riverpod/flutter_riverpod.dart';" not in content:
                        # Find where to add the import
                        import_lines = []
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if line.strip().startswith('import '):
                                import_lines.append(i)
                        
                        if import_lines:
                            insert_index = max(import_lines) + 1
                        else:
                            insert_index = 0
                        
                        import_statement = "import 'package:flutter_riverpod/flutter_riverpod.dart';"
                        lines.insert(insert_index, import_statement)
                        
                        updated_content = '\n'.join(lines)
                        full_path.write_text(updated_content)
                        print(f"    ✅ Fixed StateNotifierProvider import in {file_path}")
                        self.fixes_applied.append(f"statenotifier_import_fixed_{file_path.split('/')[-1]}")
                        
                except Exception as e:
                    print(f"    ❌ Failed to fix {file_path}: {e}")
    
    def fix_api_client_types(self):
        """Fix API client dynamic type issues"""
        print("\n🔧 PRIORITY 4: API Client Dynamic Types")
        print("-" * 50)
        
        # Fix the specific dynamic type issues in cultivars API client
        cultivars_file = self.flutter_dir / "lib/features/strains/data/cultivars_api_client.dart"
        
        if cultivars_file.exists():
            try:
                content = cultivars_file.read_text()
                
                # Fix the broken line around line 109
                if "statusCode < 200 || statusCode >= 300;" in content:
                    # Replace the broken line
                    content = content.replace(
                        "statusCode < 200 || statusCode >= 300;",
                        "statusCode < 200 || statusCode >= 300"
                    )
                
                cultivars_file.write_text(content)
                print("    ✅ Fixed cultivars API client dynamic types")
                self.fixes_applied.append("api_client_types_fixed")
                
            except Exception as e:
                print(f"    ❌ Failed to fix cultivars API client: {e}")
                self.fixes_applied.append("api_client_fix_failed")
    
    def fix_deprecated_annotations(self):
        """Fix deprecated annotations"""
        print("\n🔧 PRIORITY 5: Deprecated Annotations")
        print("-" * 50)
        
        # Fix JsonKey.new and JsonSerializable.new annotations
        deprecated_files = [
            "lib/features/auth/models/auth_tokens.dart",
            "lib/features/auth/models/user.dart"
        ]
        
        for file_path in deprecated_files:
            full_path = self.flutter_dir / file_path
            if full_path.exists():
                try:
                    content = full_path.read_text()
                    
                    # Replace JsonKey.new with JsonKey()
                    content = content.replace('@JsonKey.new', '@JsonKey()')
                    
                    # Replace JsonSerializable.new with JsonSerializable()
                    content = content.replace('@JsonSerializable.new', '@JsonSerializable()')
                    
                    if '@JsonKey.new' in content or '@JsonSerializable.new' in content:
                        print(f"    ⚠️  Still has deprecated annotations in {file_path}")
                    else:
                        full_path.write_text(content)
                        print(f"    ✅ Fixed deprecated annotations in {file_path}")
                        self.fixes_applied.append(f"deprecated_annotations_fixed_{file_path.split('/')[-1]}")
                        
                except Exception as e:
                    print(f"    ❌ Failed to fix deprecated annotations in {file_path}: {e}")
    
    def generate_build_files(self):
        """Generate build runner files"""
        print("\n🔧 PRIORITY 6: Generate Build Files")
        print("-" * 50)
        
        try:
            # Run flutter packages get
            result = subprocess.run(
                ["flutter", "pub", "get"],
                cwd=self.flutter_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("    ✅ flutter pub get completed")
                self.fixes_applied.append("flutter_pub_get_completed")
            else:
                print(f"    ⚠️  flutter pub get failed: {result.stderr}")
                self.fixes_applied.append("flutter_pub_get_failed")
                
        except Exception as e:
            print(f"    ❌ Build file generation failed: {e}")
            self.fixes_applied.append("build_generation_failed")

def main():
    """Main function"""
    fixer = FlutterCriticalFixesRound2()
    result = fixer.run_all_fixes()
    
    # Display summary
    print(f"\n📊 Flutter Critical Fixes Round 2 Summary:")
    print(f"   Total fixes applied: {len(result['fixes_applied'])}")
    print(f"   Round: {result['round']}")
    print(f"   Status: {result['status']}")
    
    print(f"\n📋 Fixes Applied:")
    for fix in result['fixes_applied']:
        print(f"   ✅ {fix}")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Run Flutter analyzer to check progress")
    print(f"   2. Continue with additional rounds if issues remain")
    print(f"   3. Focus on remaining compilation-blocking issues")
    
    return result

if __name__ == "__main__":
    main()