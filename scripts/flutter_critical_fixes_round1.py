#!/usr/bin/env python3
"""
🛠️ COMPREHENSIVE FLUTTER FIX SCRIPT - ROUND 1
Fixes the most critical Flutter analyzer issues to get compilation working
"""

import os
import re
from pathlib import Path

class FlutterCriticalFixer:
    """Fixes the most critical Flutter issues for compilation"""
    
    def __init__(self, flutter_app_dir="flutter_app"):
        self.flutter_dir = Path(flutter_app_dir)
        self.fixes_applied = []
        
    def fix_missing_imports(self):
        """Fix missing imports and undefined classes"""
        print("🔧 Fixing missing imports and undefined classes...")
        
        # Critical missing import fixes
        critical_fixes = [
            # Add missing Offset import
            {
                'file': 'lib/core/widgets/theme_widget.dart',
                'pattern': r'import \'package:flutter/material\.dart\';',
                'replacement': "import 'package:flutter/material.dart';\nimport 'package:flutter/painting.dart';"
            },
            # Fix AppTheme import
            {
                'file': 'lib/core/widgets/theme_widget.dart', 
                'pattern': r'import \'.*/app_theme\.dart\';',
                'replacement': "import '../theme/app_theme.dart';"
            },
            # Add missing API service import
            {
                'file': 'lib/screens/cultivars_list_screen.dart',
                'pattern': r'import \'.*/cultivars_api_client\.dart\';',
                'replacement': "import 'package:cultivar_app/features/strains/data/cultivars_api_client.dart';\nimport '../services/api_service.dart';"
            },
        ]
        
        for fix in critical_fixes:
            file_path = self.flutter_dir / fix['file']
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if fix['pattern'] in content:
                        content = re.sub(fix['pattern'], fix['replacement'], content)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        print(f"  ✅ Fixed imports in: {fix['file']}")
                        self.fixes_applied.append(f"import_fix_{fix['file']}")
                    else:
                        print(f"  ⚠️  Pattern not found in: {fix['file']}")
                        
                except Exception as e:
                    print(f"  ❌ Error fixing {fix['file']}: {e}")
    
    def fix_state_notifier_provider(self):
        """Fix StateNotifierProvider usage issues"""
        print("🔧 Fixing StateNotifierProvider issues...")
        
        # Fix StateNotifierProvider import and usage
        state_notifier_fixes = [
            {
                'file': 'lib/core/providers/auth_provider.dart',
                'pattern': r'import \'package:flutter_riverpod/flutter_riverpod\.dart\';',
                'replacement': "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport 'package:riverpod_annotation/riverpod_annotation.dart';"
            },
            {
                'file': 'lib/core/providers/cart_provider.dart', 
                'pattern': r'import \'package:flutter_riverpod/flutter_riverpod\.dart\';',
                'replacement': "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport 'package:riverpod_annotation/riverpod_annotation.dart';"
            },
            {
                'file': 'lib/core/providers/cultivar_provider.dart',
                'pattern': r'import \'package:flutter_riverpod/flutter_riverpod\.dart\';',
                'replacement': "import 'package:flutter_riverpod/flutter_riverpod.dart';\nimport 'package:riverpod_annotation/riverpod_annotation.dart';"
            }
        ]
        
        for fix in state_notifier_fixes:
            file_path = self.flutter_dir / fix['file']
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    content = re.sub(fix['pattern'], fix['replacement'], content)
                    with open(file_path, 'w') as f:
                        f.write(content)
                    print(f"  ✅ Fixed StateNotifierProvider imports in: {fix['file']}")
                    self.fixes_applied.append(f"state_notifier_fix_{fix['file']}")
                    
                except Exception as e:
                    print(f"  ❌ Error fixing StateNotifierProvider in {fix['file']}: {e}")
    
    def fix_api_client_types(self):
        """Fix API client dynamic type issues"""
        print("🔧 Fixing API client type issues...")
        
        # Fix dynamic type issues in API clients
        api_client_fixes = [
            {
                'file': 'lib/features/dashboard/data/dashboard_api_client.dart',
                'pattern': r'dynamic.*response',
                'replacement': 'Map<String, dynamic> response'
            },
            {
                'file': 'lib/features/strains/data/cultivars_api_client.dart',
                'pattern': r'dynamic.*data',
                'replacement': 'Map<String, dynamic> data'
            },
            {
                'file': 'lib/features/strains/data/cultivars_api_client.dart',
                'pattern': r'dynamic.*params',
                'replacement': 'Map<String, dynamic> params'
            }
        ]
        
        for fix in api_client_fixes:
            file_path = self.flutter_dir / fix['file']
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Count matches
                    matches = len(re.findall(fix['pattern'], content))
                    if matches > 0:
                        content = re.sub(fix['pattern'], fix['replacement'], content)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        print(f"  ✅ Fixed {matches} dynamic type issues in: {fix['file']}")
                        self.fixes_applied.append(f"api_type_fix_{fix['file']}")
                        
                except Exception as e:
                    print(f"  ❌ Error fixing API types in {fix['file']}: {e}")
    
    def fix_deprecated_annotations(self):
        """Fix deprecated JsonKey and JsonSerializable annotations"""
        print("🔧 Fixing deprecated annotations...")
        
        # Fix JsonKey.new to @JsonKey()
        json_key_fixes = [
            {
                'file_pattern': 'lib/**/*.dart',
                'find': r'@JsonKey\.new',
                'replace': '@JsonKey()'
            },
            {
                'file_pattern': 'lib/**/*.dart', 
                'find': r'@JsonSerializable\.new',
                'replace': '@JsonSerializable()'
            }
        ]
        
        for fix in json_key_fixes:
            # Find all Dart files in lib directory
            dart_files = list(self.flutter_dir.glob('**/*.dart'))
            
            for file_path in dart_files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if fix['find'] in content:
                        content = re.sub(fix['find'], fix['replace'], content)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        print(f"  ✅ Fixed deprecated annotations in: {file_path.name}")
                        self.fixes_applied.append(f"deprecated_fix_{file_path.name}")
                        
                except Exception as e:
                    print(f"  ❌ Error fixing deprecated annotations in {file_path.name}: {e}")
    
    def add_missing_pubspec_deps(self):
        """Add missing pubspec dependencies"""
        print("🔧 Adding missing pubspec dependencies...")
        
        pubspec_path = self.flutter_dir / 'pubspec.yaml'
        if pubspec_path.exists():
            try:
                with open(pubspec_path, 'r') as f:
                    content = f.read()
                
                # Add missing dependencies
                missing_deps = [
                    "  riverpod_annotation: ^2.3.3",
                    "  freezed_annotation: ^2.4.1",
                    "  json_annotation: ^4.8.1",
                    "  go_router: ^14.0.2",
                    "  image_picker: ^1.0.4",
                    "  http: ^1.1.2"
                ]
                
                dependencies_section = "dependencies:"
                if dependencies_section in content:
                    # Find end of dependencies section
                    deps_end = content.find('\ndev_dependencies:')
                    if deps_end == -1:
                        deps_end = len(content)
                    
                    # Check if each dependency is missing and add it
                    for dep in missing_deps:
                        if dep.split(':')[0].strip() not in content:
                            content = content[:deps_end] + f"\n{dep}" + content[deps_end:]
                            print(f"  ✅ Added dependency: {dep}")
                            self.fixes_applied.append(f"pubspec_dep_{dep}")
                    
                    with open(pubspec_path, 'w') as f:
                        f.write(content)
                        
            except Exception as e:
                print(f"  ❌ Error updating pubspec.yaml: {e}")
    
    def create_missing_models(self):
        """Create missing model classes"""
        print("🔧 Creating missing model classes...")
        
        # Create missing AppSettings class
        app_settings_path = self.flutter_dir / 'lib/core/models/app_settings.dart'
        if not app_settings_path.exists():
            app_settings_content = """import 'package:freezed_annotation/freezed_annotation.dart';

part 'app_settings.freezed.dart';
part 'app_settings.g.dart';

@freezed
class AppSettings with _$AppSettings {
  const factory AppSettings({
    @Default('en') String language,
    @Default(true) bool notifications,
    @Default(true) bool darkMode,
    @Default(1) int theme,
  }) = _AppSettings;
  
  factory AppSettings.fromJson(Map<String, dynamic> json) =>
      _$AppSettingsFromJson(json);
}
"""
            with open(app_settings_path, 'w') as f:
                f.write(app_settings_content)
            print("  ✅ Created AppSettings model")
            self.fixes_applied.append("app_settings_model")
        
        # Create missing CartProviderState class
        cart_state_path = self.flutter_dir / 'lib/core/models/cart_state.dart'
        if not cart_state_path.exists():
            cart_state_content = """import 'package:freezed_annotation/freezed_annotation.dart';
import 'cart_models.dart';

part 'cart_state.freezed.dart';
part 'cart_state.g.dart';

@freezed
class CartProviderState with _$CartProviderState {
  const factory CartProviderState({
    @Default([]) List<CartItem> items,
    @Default(0) int itemCount,
    @Default(0.0) double total,
    @Default(true) bool isLoading,
    @Default(null) String? error,
  }) = _CartProviderState;
  
  factory CartProviderState.fromJson(Map<String, dynamic> json) =>
      _$CartProviderStateFromJson(json);
}
"""
            with open(cart_state_path, 'w') as f:
                f.write(cart_state_content)
            print("  ✅ Created CartProviderState model")
            self.fixes_applied.append("cart_state_model")
    
    def fix_const_constructors(self):
        """Fix prefer_const_constructors issues"""
        print("🔧 Fixing const constructor issues...")
        
        # Fix Environment constructor calls
        env_fixes = [
            {
                'file': 'lib/config/environment.dart',
                'pattern': r'Environment\(\)',
                'replacement': 'const Environment()'
            },
            {
                'file': 'lib/config/environment.dart',
                'pattern': r'Environment\(',
                'replacement': 'const Environment('
            }
        ]
        
        for fix in env_fixes:
            file_path = self.flutter_dir / fix['file']
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    if fix['pattern'] in content:
                        content = re.sub(fix['pattern'], fix['replacement'], content)
                        with open(file_path, 'w') as f:
                            f.write(content)
                        print(f"  ✅ Fixed const constructors in: {fix['file']}")
                        self.fixes_applied.append(f"const_fix_{fix['file']}")
                        
                except Exception as e:
                    print(f"  ❌ Error fixing const constructors in {fix['file']}: {e}")
    
    def run_all_fixes(self):
        """Run all critical fixes"""
        print("🛠️  Starting Flutter Critical Fixes - Round 1")
        print("=" * 60)
        
        self.add_missing_pubspec_deps()
        self.create_missing_models()
        self.fix_missing_imports()
        self.fix_state_notifier_provider()
        self.fix_api_client_types()
        self.fix_deprecated_annotations()
        self.fix_const_constructors()
        
        print("\n📊 Flutter Fixes Summary:")
        print(f"   Total fixes applied: {len(self.fixes_applied)}")
        
        if self.fixes_applied:
            print(f"\n📋 Fixes Applied:")
            for fix in self.fixes_applied:
                print(f"   ✅ {fix}")
        
        return self.fixes_applied

def main():
    """Main function"""
    fixer = FlutterCriticalFixer()
    fixes = fixer.run_all_fixes()
    
    print("\n🚀 Next Steps:")
    print("1. Run flutter pub get to install new dependencies")
    print("2. Run flutter analyze again to check remaining issues")
    print("3. Fix any remaining compilation errors")
    
    return fixes

if __name__ == "__main__":
    main()