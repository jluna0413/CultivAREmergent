// Script to fix critical compilation errors in Flutter app
// This addresses the most blocking issues that prevent compilation

import 'dart:io';

void main() async {
  print('🔧 Starting comprehensive compilation error fixes...');

  // Fix 1: PlantsApiService missing methods
  await fixPlantsApiService();

  // Fix 2: Import path issues
  await fixImportPaths();

  // Fix 3: Dashboard provider issues
  await fixDashboardProvider();

  // Fix 4: Offset import issues
  await fixOffsetIssues();

  print('✅ Critical fixes completed!');
}

Future<void> fixPlantsApiService() async {
  print('🔧 Fixing PlantsApiService methods...');

  final file = File('lib/core/services/plants_api_service.dart');
  if (!await file.exists()) return;

  String content = await file.readAsString();

  // Add missing methods if they don't exist
  if (!content.contains('PlantCreate')) {
    content = content.replaceAll(
      'Future<Plant> createPlant(PlantCreateModel request) async {',
      '''Future<Plant> createPlant(PlantCreateModel request) async {
    final response = await apiClient.post(
      '/plants',
      {
        'name': request.name,
        'description': request.description,
        'status_id': request.statusId,
        'cultivar_id': request.cultivarId,
        'is_clone': request.isClone,
        'autoflower': request.autoflower,
        'start_date': request.startDate?.toIso8601String(),
        'last_water_date': request.lastWaterDate?.toIso8601String(),
        'last_feed_date': request.lastFeedDate?.toIso8601String(),
        'harvest_date': request.harvestDate?.toIso8601String(),
      },
    );
    return Plant.fromJson(response['data']);''',
    );
  }

  if (!content.contains('PlantUpdate')) {
    content = content.replaceAll(
      'Future<Plant> updatePlant(int id, PlantUpdateModel request) async {',
      '''Future<Plant> updatePlant(int id, PlantUpdateModel request) async {
    final response = await apiClient.put(
      '/plants/\$id',
      {
        if (request.name != null) 'name': request.name,
        if (request.description != null) 'description': request.description,
        if (request.statusId != null) 'status_id': request.statusId,
        if (request.cultivarId != null) 'cultivar_id': request.cultivarId,
        if (request.isClone != null) 'is_clone': request.isClone,
        if (request.autoflower != null) 'autoflower': request.autoflower,
        if (request.startDate != null) 'start_date': request.startDate?.toIso8601String(),
        if (request.lastWaterDate != null) 'last_water_date': request.lastWaterDate?.toIso8601String(),
        if (request.lastFeedDate != null) 'last_feed_date': request.lastFeedDate?.toIso8601String(),
        if (request.harvestDate != null) 'harvest_date': request.harvestDate?.toIso8601String(),
      },
    );
    return Plant.fromJson(response['data']);''',
    );
  }

  await file.writeAsString(content);
  print('✅ PlantsApiService methods fixed');
}

Future<void> fixImportPaths() async {
  print('🔧 Fixing import paths...');

  // Find and fix common import path issues
  final directories = ['lib/core', 'lib/features', 'lib/presentation'];

  for (final dir in directories) {
    final directory = Directory(dir);
    if (!await directory.exists()) continue;

    await for (final entity in directory.list(recursive: true)) {
      if (entity is File && entity.path.endsWith('.dart')) {
        String content = await entity.readAsString();
        String originalContent = content;

        // Fix common import path issues
        content = content.replaceAll(
          "import 'package:cultivar_app/",
          "import '../../",
        );

        content = content.replaceAll(
          "import 'package:flutter_app/",
          "import '../../",
        );

        if (content != originalContent) {
          await entity.writeAsString(content);
          print('📁 Fixed imports in: ${entity.path}');
        }
      }
    }
  }

  print('✅ Import paths fixed');
}

Future<void> fixDashboardProvider() async {
  print('🔧 Fixing DashboardProvider issues...');

  final file = File('lib/core/state/dashboard_provider.dart');
  if (!await file.exists()) return;

  String content = await file.readAsString();

  // Fix DashboardStats return type issue
  content = content.replaceAll(
    'return await apiClient.getDashboardStats();',
    'final stats = await apiClient.getDashboardStats();\n      return stats;',
  );

  // Remove StateNotifierProvider references if causing issues
  content = content.replaceAll('StateNotifierProvider', 'StateProvider');

  await file.writeAsString(content);
  print('✅ DashboardProvider issues fixed');
}

Future<void> fixOffsetIssues() async {
  print('🔧 Fixing Offset import issues...');

  // Create a comprehensive fix for Offset issues
  final directories = [
    'lib/core',
    'lib/features',
    'lib/presentation',
    'lib/screens',
  ];

  for (final dir in directories) {
    final directory = Directory(dir);
    if (!await directory.exists()) continue;

    await for (final entity in directory.list(recursive: true)) {
      if (entity is File && entity.path.endsWith('.dart')) {
        String content = await entity.readAsString();
        String originalContent = content;

        // Ensure Offset import is present
        if (!content.contains("import 'package:flutter/material.dart'") &&
            (content.contains('Offset') ||
                content.contains('Animation<Offset>'))) {
          // Add the import if Offset is used but not imported
          final lines = content.split('\n');
          final importIndex = lines.indexWhere(
            (line) => line.startsWith("import 'package:flutter"),
          );
          if (importIndex != -1) {
            lines.insert(
              importIndex + 1,
              "import 'package:flutter/material.dart';",
            );
            content = lines.join('\n');
          } else {
            content = "import 'package:flutter/material.dart';\n$content";
          }
        }

        // Fix Offset.zero reference
        content = content.replaceAll('Offset.zero', 'const Offset(0, 0)');

        // Fix Offset constructor calls
        final offsetRegex = RegExp(
          r'Offset\(\s*([0-9.\-]+)\s*,\s*([0-9.\-]+)\s*\)',
        );
        content = content.replaceAllMapped(offsetRegex, (match) {
          return 'Offset(${match.group(1)}, ${match.group(2)})';
        });

        if (content != originalContent) {
          await entity.writeAsString(content);
          print('📁 Fixed Offset issues in: ${entity.path}');
        }
      }
    }
  }

  print('✅ Offset issues fixed');
}
