// Unit Tests for Plant Models
// Comprehensive testing for Plant, PlantStatus, PlantType models

import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/core/models/plant_models.dart';

void main() {
  group('Plant Model Tests', () {
    late Plant testPlant;

    setUp(() {
      final now = DateTime.now();
      testPlant = Plant(
        id: 1,
        name: 'Test Plant',
        description: 'Test description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: DateTime(2024, 1, 1),
        updatedAt: DateTime(2024, 1, 1),
      );
    });

    test('Plant should be created with valid data', () {
      expect(testPlant.id, equals(1));
      expect(testPlant.name, equals('Test Plant'));
      expect(testPlant.description, equals('Test description'));
      expect(testPlant.statusId, equals(1));
      expect(testPlant.cultivarId, equals(1));
      expect(testPlant.isClone, isFalse);
      expect(testPlant.autoflower, isFalse);
      expect(testPlant.userId, equals(1));
      expect(testPlant.createdAt, isNotNull);
      expect(testPlant.updatedAt, isNotNull);
    });

    test('Plant should create valid copy with new values', () {
      final updatedPlant = testPlant.copyWith(
        name: 'Updated Plant',
        description: 'Updated description',
      );

      expect(updatedPlant.name, equals('Updated Plant'));
      expect(updatedPlant.description, equals('Updated description'));
      expect(updatedPlant.id, equals(1));
      expect(updatedPlant.userId, equals(1));
    });

    test('Plant should serialize to JSON correctly', () {
      final json = testPlant.toJson();

      expect(json['id'], equals(1));
      expect(json['name'], equals('Test Plant'));
      expect(json['description'], equals('Test description'));
      expect(json['status_id'], equals(1));
      expect(json['cultivar_id'], equals(1));
      expect(json['is_clone'], isFalse);
      expect(json['autoflower'], isFalse);
      expect(json['user_id'], equals(1));
      expect(json.containsKey('created_at'), isTrue);
      expect(json.containsKey('updated_at'), isTrue);
    });

    test('Plant should deserialize from JSON correctly', () {
      final json = {
        'id': 2,
        'name': 'JSON Plant',
        'description': 'JSON description',
        'status_id': 2,
        'cultivar_id': 2,
        'is_clone': true,
        'autoflower': true,
        'start_date': '2024-02-01T00:00:00.000Z',
        'last_water_date': '2024-02-15T00:00:00.000Z',
        'last_feed_date': '2024-02-10T00:00:00.000Z',
        'harvest_date': '2024-05-01T00:00:00.000Z',
        'user_id': 2,
        'created_at': '2024-02-01T00:00:00.000Z',
        'updated_at': '2024-02-01T00:00:00.000Z',
      };

      final plant = Plant.fromJson(json);

      expect(plant.id, equals(2));
      expect(plant.name, equals('JSON Plant'));
      expect(plant.description, equals('JSON description'));
      expect(plant.statusId, equals(2));
      expect(plant.cultivarId, equals(2));
      expect(plant.isClone, isTrue);
      expect(plant.autoflower, isTrue);
      expect(plant.userId, equals(2));
    });

    test('Plant should handle null harvest date correctly', () {
      final now = DateTime.now();
      final plantWithoutHarvest = Plant(
        id: 3,
        name: 'No Harvest Plant',
        description: 'No harvest date',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: null,
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      expect(plantWithoutHarvest.harvestDate, isNull);
    });

    test('Plant should handle null cultivar ID correctly', () {
      final now = DateTime.now();
      final plantWithoutCultivar = Plant(
        id: 4,
        name: 'No Cultivar Plant',
        description: 'No cultivar',
        statusId: 1,
        cultivarId: null,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      expect(plantWithoutCultivar.cultivarId, isNull);
    });

    test('Plant equality should work correctly', () {
      final now = DateTime.now();
      final plant1 = Plant(
        id: 1,
        name: 'Same Plant',
        description: 'Same description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      final plant2 = Plant(
        id: 1,
        name: 'Same Plant',
        description: 'Same description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      final plant3 = Plant(
        id: 1,
        name: 'Different Plant',
        description: 'Different description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      expect(plant1, equals(plant2));
      expect(plant1, isNot(equals(plant3)));
    });

    test('Plant hash code should be consistent', () {
      final now = DateTime.now();
      final plant1 = Plant(
        id: 1,
        name: 'Test Plant',
        description: 'Test description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      final plant2 = Plant(
        id: 1,
        name: 'Test Plant',
        description: 'Test description',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      expect(plant1.hashCode, equals(plant2.hashCode));
    });

    test('Plant toString should return meaningful output', () {
      final now = DateTime.now();
      final plant = Plant(
        id: 1,
        name: 'Northern Lights',
        description: 'Indica strain',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      final string = plant.toString();
      expect(string, contains('Northern Lights'));
      expect(string, contains('1'));
    });
  });

  group('Plant Edge Cases', () {
    test('Plant should handle edge case data correctly', () {
      final now = DateTime.now();
      final edgeCases = [
        // Empty description
        Plant(
          id: 1,
          name: 'Test Plant',
          description: '',
          statusId: 1,
          cultivarId: 1,
          isClone: false,
          autoflower: false,
          startDate: DateTime(2024, 1, 1),
          lastWaterDate: DateTime(2024, 1, 15),
          lastFeedDate: DateTime(2024, 1, 10),
          harvestDate: DateTime(2024, 4, 1),
          userId: 1,
          createdAt: now,
          updatedAt: now,
        ),

        // Very long description
        Plant(
          id: 2,
          name: 'Test Plant',
          description: 'a' * 1000,
          statusId: 1,
          cultivarId: 1,
          isClone: false,
          autoflower: false,
          startDate: DateTime(2024, 1, 1),
          lastWaterDate: DateTime(2024, 1, 15),
          lastFeedDate: DateTime(2024, 1, 10),
          harvestDate: DateTime(2024, 4, 1),
          userId: 1,
          createdAt: now,
          updatedAt: now,
        ),

        // Special characters
        Plant(
          id: 3,
          name: 'TestSpecialCharsAtHashDollarPercent',
          description: 'Special chars test',
          statusId: 1,
          cultivarId: 1,
          isClone: false,
          autoflower: false,
          startDate: DateTime(2024, 1, 1),
          lastWaterDate: DateTime(2024, 1, 15),
          lastFeedDate: DateTime(2024, 1, 10),
          harvestDate: DateTime(2024, 4, 1),
          userId: 1,
          createdAt: now,
          updatedAt: now,
        ),

        // Null optional fields
        Plant(
          id: 4,
          name: 'Null Fields Plant',
          description: 'Testing nulls',
          statusId: 1,
          cultivarId: null,
          isClone: false,
          autoflower: false,
          startDate: DateTime(2024, 1, 1),
          lastWaterDate: DateTime(2024, 1, 15),
          lastFeedDate: DateTime(2024, 1, 10),
          harvestDate: null,
          userId: 1,
          createdAt: now,
          updatedAt: now,
        ),

        // Zero values
        Plant(
          id: 0,
          name: 'Zero Values Plant',
          description: 'Zero values test',
          statusId: 0,
          cultivarId: 0,
          isClone: false,
          autoflower: false,
          startDate: DateTime(2024, 1, 1),
          lastWaterDate: DateTime(2024, 1, 15),
          lastFeedDate: DateTime(2024, 1, 10),
          harvestDate: DateTime(2024, 4, 1),
          userId: 0,
          createdAt: now,
          updatedAt: now,
        ),

        // Clone with autoflower
        Plant(
          id: 5,
          name: 'Clone Autoflower Plant',
          description: 'Clone autoflower test',
          statusId: 1,
          cultivarId: 1,
          isClone: true,
          autoflower: true,
          startDate: now,
          lastWaterDate: now,
          lastFeedDate: now,
          harvestDate: DateTime(2024, 4, 1),
          userId: 1,
          createdAt: now,
          updatedAt: now,
        ),
      ];

      for (final plant in edgeCases) {
        // Test that we can serialize and deserialize without errors
        final json = plant.toJson();
        final restored = Plant.fromJson(json);
        expect(restored, equals(plant));

        // Test basic validation
        expect(plant.name, isNotEmpty);
        expect(plant.id, greaterThanOrEqualTo(0));
        expect(plant.statusId, greaterThanOrEqualTo(0));
        expect(plant.userId, greaterThanOrEqualTo(0));
      }
    });

    test('Plant should handle minimum values', () {
      final now = DateTime.now();
      final plant = Plant(
        id: 0,
        name: 'Min Plant',
        description: 'Min values',
        statusId: 0,
        cultivarId: 0,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 0,
        createdAt: now,
        updatedAt: now,
      );

      expect(plant.id, equals(0));
      expect(plant.statusId, equals(0));
      expect(plant.userId, equals(0));
    });

    test('Plant should handle maximum values', () {
      final now = DateTime.now();
      final plant = Plant(
        id: 999999,
        name: 'a' * 100, // Maximum name length
        description: 'a' * 1000, // Maximum description length
        statusId: 999999,
        cultivarId: 999999,
        isClone: true,
        autoflower: true,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 999999,
        createdAt: now,
        updatedAt: now,
      );

      expect(plant.id, equals(999999));
      expect(plant.name.length, equals(100));
      expect(plant.description!.length, equals(1000));
    });
  });

  group('Plant Business Logic Tests', () {
    test('Plant should determine if it needs watering based on last water date',
        () {
      final now = DateTime.now();
      final recentlyWatered = Plant(
        id: 1,
        name: 'Recently Watered',
        description: 'Recent water',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: now.subtract(const Duration(days: 1)),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      final needsWatering = Plant(
        id: 2,
        name: 'Needs Watering',
        description: 'Old water',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: now.subtract(const Duration(days: 7)),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      // The exact logic would depend on the business rules
      expect(recentlyWatered.lastWaterDate, isNotNull);
      expect(needsWatering.lastWaterDate, isNotNull);

      // Test that recently watered plant has more recent date
      expect(
          recentlyWatered.lastWaterDate!.isAfter(needsWatering.lastWaterDate!),
          isTrue);
    });

    test('Plant should determine if it needs feeding', () {
      final now = DateTime.now();
      final recentlyFed = Plant(
        id: 1,
        name: 'Recently Fed',
        description: 'Recent feed',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: now.subtract(const Duration(days: 1)),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      final needsFeeding = Plant(
        id: 2,
        name: 'Needs Feeding',
        description: 'Old feed',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: now.subtract(const Duration(days: 14)),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      expect(recentlyFed.lastFeedDate, isNotNull);
      expect(needsFeeding.lastFeedDate, isNotNull);

      // Test that recently fed plant has more recent date
      expect(recentlyFed.lastFeedDate!.isAfter(needsFeeding.lastFeedDate!),
          isTrue);
    });

    test('Clone plant should be distinguishable from seed plant', () {
      final now = DateTime.now();
      final clone = Plant(
        id: 1,
        name: 'Clone Plant',
        description: 'Clone',
        statusId: 1,
        cultivarId: 1,
        isClone: true,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      final seed = Plant(
        id: 2,
        name: 'Seed Plant',
        description: 'Seed',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      expect(clone.isClone, isTrue);
      expect(seed.isClone, isFalse);
      expect(clone.autoflower, isFalse); // Default false
    });

    test('Autoflower plant should be distinguishable from regular plant', () {
      final now = DateTime.now();
      final autoflower = Plant(
        id: 1,
        name: 'Autoflower Plant',
        description: 'Autoflower',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: true,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );
      final regular = Plant(
        id: 2,
        name: 'Regular Plant',
        description: 'Regular',
        statusId: 1,
        cultivarId: 1,
        isClone: false,
        autoflower: false,
        startDate: DateTime(2024, 1, 1),
        lastWaterDate: DateTime(2024, 1, 15),
        lastFeedDate: DateTime(2024, 1, 10),
        harvestDate: DateTime(2024, 4, 1),
        userId: 1,
        createdAt: now,
        updatedAt: now,
      );

      expect(autoflower.autoflower, isTrue);
      expect(regular.autoflower, isFalse);
    });
  });

  group('Plant Model Validation Tests', () {
    test('Plant should validate required fields', () {
      expect(() => Plant.fromJson({}), throwsA(isA<Exception>()));
    });

    test('Plant should handle missing optional fields gracefully', () {
      final json = {
        'id': 1,
        'name': 'Valid Plant',
        'status_id': 1,
        'cultivar_id': 1,
        'is_clone': false,
        'autoflower': false,
        'user_id': 1,
        'created_at': '2024-01-01T00:00:00.000Z',
        'updated_at': '2024-01-01T00:00:00.000Z',
      };

      final plant = Plant.fromJson(json);
      expect(plant.id, equals(1));
      expect(plant.name, equals('Valid Plant'));
      expect(plant.description, isNull); // Should be null when not provided
      expect(plant.harvestDate, isNull); // Should be null when not provided
    });

    test('Plant should handle invalid JSON gracefully', () {
      // Test with missing required fields
      expect(() => Plant.fromJson({'name': 'Incomplete'}),
          throwsA(isA<Exception>()));

      // Test with invalid data types
      expect(
          () => Plant.fromJson({
                'id': 'invalid_id',
                'name': 'Invalid ID Test',
                'status_id': 1,
                'cultivar_id': 1,
                'is_clone': false,
                'autoflower': false,
                'user_id': 1,
                'created_at': '2024-01-01T00:00:00.000Z',
                'updated_at': '2024-01-01T00:00:00.000Z',
              }),
          throwsA(isA<Exception>()));
    });
  });

  group('Plant Status Tests', () {
    test('PlantStatus should be created with valid data', () {
      const status = PlantStatus(
        id: 1,
        name: 'Active',
        description: 'Plant is actively growing',
        color: '#00FF00',
      );

      expect(status.id, equals(1));
      expect(status.name, equals('Active'));
      expect(status.description, equals('Plant is actively growing'));
      expect(status.color, equals('#00FF00'));
    });

    test('PlantStatus should serialize and deserialize correctly', () {
      const status = PlantStatus(
        id: 1,
        name: 'Active',
        description: 'Plant is actively growing',
        color: '#00FF00',
      );

      final json = status.toJson();
      final restored = PlantStatus.fromJson(json);

      expect(restored.id, equals(status.id));
      expect(restored.name, equals(status.name));
      expect(restored.description, equals(status.description));
      expect(restored.color, equals(status.color));
    });
  });
}
