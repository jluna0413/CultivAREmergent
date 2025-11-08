// Unit Tests for Core Models - Comprehensive model validation
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/models/plant.dart';
import 'package:cultivar_app/models/cultivar.dart';

void main() {
  group('Model Tests', () {
    // Cultivar Models Tests
    group('Cultivar Models', () {
      test('should create valid Cultivar model with required fields', () {
        final cultivar = Cultivar(
          userId: 1,
          name: 'Northern Lights',
          indica: 80,
          sativa: 20,
          autoflower: false,
          seedCount: 10,
        );

        expect(cultivar.userId, 1);
        expect(cultivar.name, 'Northern Lights');
        expect(cultivar.indica, 80);
        expect(cultivar.sativa, 20);
        expect(cultivar.autoflower, false);
        expect(cultivar.seedCount, 10);
        expect(cultivar.plantCount, 0); // default value
      });

      test('should create Cultivar model with optional fields', () {
        final cultivar = Cultivar(
          id: 123,
          userId: 1,
          name: 'Northern Lights',
          breederId: 456,
          breederName: 'Sensi Seeds',
          indica: 80,
          sativa: 20,
          autoflower: false,
          description: 'Classic indica strain',
          shortDescription: 'Classic indica',
          seedCount: 10,
          cycleTime: 60,
          url: 'https://example.com/strain',
          plantCount: 5,
        );

        expect(cultivar.id, 123);
        expect(cultivar.userId, 1);
        expect(cultivar.name, 'Northern Lights');
        expect(cultivar.breederId, 456);
        expect(cultivar.breederName, 'Sensi Seeds');
        expect(cultivar.indica, 80);
        expect(cultivar.sativa, 20);
        expect(cultivar.autoflower, false);
        expect(cultivar.description, 'Classic indica strain');
        expect(cultivar.shortDescription, 'Classic indica');
        expect(cultivar.seedCount, 10);
        expect(cultivar.cycleTime, 60);
        expect(cultivar.url, 'https://example.com/strain');
        expect(cultivar.plantCount, 5);
      });

      test('should create Cultivar from JSON', () {
        final json = {
          'id': 123,
          'user_id': 1,
          'name': 'Northern Lights',
          'breeder_id': 456,
          'breeder_name': 'Sensi Seeds',
          'indica': 80,
          'sativa': 20,
          'autoflower': false,
          'description': 'Classic indica strain',
          'short_description': 'Classic indica',
          'seed_count': 10,
          'cycle_time': 60,
          'url': 'https://example.com/strain',
          'plant_count': 5,
        };

        final cultivar = Cultivar.fromJson(json);

        expect(cultivar.id, 123);
        expect(cultivar.userId, 1);
        expect(cultivar.name, 'Northern Lights');
        expect(cultivar.breederId, 456);
        expect(cultivar.breederName, 'Sensi Seeds');
        expect(cultivar.indica, 80);
        expect(cultivar.sativa, 20);
        expect(cultivar.autoflower, false);
        expect(cultivar.description, 'Classic indica strain');
        expect(cultivar.shortDescription, 'Classic indica');
        expect(cultivar.seedCount, 10);
        expect(cultivar.cycleTime, 60);
        expect(cultivar.url, 'https://example.com/strain');
        expect(cultivar.plantCount, 5);
      });

      test('should convert Cultivar to JSON', () {
        final cultivar = Cultivar(
          id: 123,
          userId: 1,
          name: 'Northern Lights',
          breederId: 456,
          breederName: 'Sensi Seeds',
          indica: 80,
          sativa: 20,
          autoflower: false,
          description: 'Classic indica strain',
          shortDescription: 'Classic indica',
          seedCount: 10,
          cycleTime: 60,
          url: 'https://example.com/strain',
          plantCount: 5,
        );

        final json = cultivar.toJson();

        expect(json['id'], 123);
        expect(json['user_id'], 1);
        expect(json['name'], 'Northern Lights');
        expect(json['breeder_id'], 456);
        expect(json['breeder_name'], 'Sensi Seeds');
        expect(json['indica'], 80);
        expect(json['sativa'], 20);
        expect(json['autoflower'], false);
        expect(json['description'], 'Classic indica strain');
        expect(json['short_description'], 'Classic indica');
        expect(json['seed_count'], 10);
        expect(json['cycle_time'], 60);
        expect(json['url'], 'https://example.com/strain');
        expect(json['plant_count'], 5);
      });

      test('should copy Cultivar with updated values', () {
        final original = Cultivar(
          userId: 1,
          name: 'Northern Lights',
          indica: 80,
          sativa: 20,
          autoflower: false,
          seedCount: 10,
        );

        final copied = original.copyWith(
          name: 'Northern Lights #5',
          indica: 70,
          sativa: 30,
        );

        expect(copied.userId, 1); // unchanged
        expect(copied.name, 'Northern Lights #5'); // updated
        expect(copied.indica, 70); // updated
        expect(copied.sativa, 30); // updated
        expect(copied.autoflower, false); // unchanged
        expect(copied.seedCount, 10); // unchanged
      });

      test('should compare Cultivar objects correctly', () {
        final cultivar1 = Cultivar(
          id: 123,
          userId: 1,
          name: 'Northern Lights',
          indica: 80,
          sativa: 20,
          autoflower: false,
          seedCount: 10,
        );

        final cultivar2 = Cultivar(
          id: 123,
          userId: 1,
          name: 'Northern Lights',
          indica: 80,
          sativa: 20,
          autoflower: false,
          seedCount: 10,
        );

        final cultivar3 = Cultivar(
          id: 456,
          userId: 1,
          name: 'White Widow',
          indica: 60,
          sativa: 40,
          autoflower: false,
          seedCount: 10,
        );

        expect(cultivar1 == cultivar2, true); // same ID
        expect(cultivar1 == cultivar3, false); // different ID
        expect(cultivar1.hashCode, cultivar2.hashCode);
      });

      test('should provide correct string representation', () {
        final cultivar = Cultivar(
          id: 123,
          userId: 1,
          name: 'Northern Lights',
          breederName: 'Sensi Seeds',
          indica: 80,
          sativa: 20,
          autoflower: false,
          seedCount: 10,
        );

        expect(cultivar.toString(),
            'Cultivar(id: 123, name: Northern Lights, breeder: Sensi Seeds)');
      });
    });

    // Plant Models Tests
    group('Plant Models', () {
      test('should create valid CreatePlantRequest model', () {
        final createRequest = CreatePlantRequest(
          name: 'White Widow',
          cultivarName: 'Northern Lights',
          strain: 'Indica Dominant',
          plantedDate: DateTime(2024, 1, 15),
          location: 'Grow Room A',
          notes: 'First planting',
          seedBank: 'Sensi Seeds',
          breeder: 'Sensi Seeds',
        );

        expect(createRequest.name, 'White Widow');
        expect(createRequest.cultivarName, 'Northern Lights');
        expect(createRequest.strain, 'Indica Dominant');
        expect(createRequest.plantedDate, DateTime(2024, 1, 15));
        expect(createRequest.location, 'Grow Room A');
        expect(createRequest.notes, 'First planting');
        expect(createRequest.seedBank, 'Sensi Seeds');
        expect(createRequest.breeder, 'Sensi Seeds');
      });

      test('should create CreatePlantRequest with minimal required fields', () {
        const createRequest = CreatePlantRequest(
          name: 'White Widow',
        );

        expect(createRequest.name, 'White Widow');
        expect(createRequest.cultivarName, null);
        expect(createRequest.strain, null);
        expect(createRequest.plantedDate, null);
        expect(createRequest.location, null);
        expect(createRequest.notes, null);
        expect(createRequest.seedBank, null);
        expect(createRequest.breeder, null);
      });

      test('should convert CreatePlantRequest to JSON', () {
        final createRequest = CreatePlantRequest(
          name: 'White Widow',
          cultivarName: 'Northern Lights',
          plantedDate: DateTime(2024, 1, 15),
          notes: 'First planting',
        );

        final json = createRequest.toJson();

        expect(json['name'], 'White Widow');
        expect(json['cultivar_name'], 'Northern Lights');
        expect(json['strain'], null);
        expect(json['planted_date'], '2024-01-15T00:00:00.000');
        expect(json['location'], null);
        expect(json['notes'], 'First planting');
        expect(json['seed_bank'], null);
        expect(json['breeder'], null);
      });

      test('should create CreatePlantRequest from JSON', () {
        final json = {
          'name': 'White Widow',
          'cultivar_name': 'Northern Lights',
          'strain': 'Indica Dominant',
          'planted_date': '2024-01-15T00:00:00.000',
          'location': 'Grow Room A',
          'notes': 'First planting',
          'seed_bank': 'Sensi Seeds',
          'breeder': 'Sensi Seeds',
        };

        final createRequest = CreatePlantRequest.fromJson(json);

        expect(createRequest.name, 'White Widow');
        expect(createRequest.cultivarName, 'Northern Lights');
        expect(createRequest.strain, 'Indica Dominant');
        expect(createRequest.plantedDate, DateTime(2024, 1, 15));
        expect(createRequest.location, 'Grow Room A');
        expect(createRequest.notes, 'First planting');
        expect(createRequest.seedBank, 'Sensi Seeds');
        expect(createRequest.breeder, 'Sensi Seeds');
      });

      test('should create valid Plant model', () {
        final plant = Plant(
          id: 1,
          name: 'Northern Lights #5',
          cultivarName: 'Northern Lights',
          strain: 'Indica',
          plantedDate: DateTime(2024, 1, 1),
          createdAt: DateTime(2024, 1, 1),
          updatedAt: DateTime(2024, 1, 1),
          location: 'Grow Room A',
          notes: 'Auto-flowering plant',
          seedBank: 'Sensi Seeds',
          breeder: 'Sensi Seeds',
          status: 'flowering',
        );

        expect(plant.id, 1);
        expect(plant.name, 'Northern Lights #5');
        expect(plant.cultivarName, 'Northern Lights');
        expect(plant.strain, 'Indica');
        expect(plant.plantedDate, DateTime(2024, 1, 1));
        expect(plant.createdAt, DateTime(2024, 1, 1));
        expect(plant.updatedAt, DateTime(2024, 1, 1));
        expect(plant.location, 'Grow Room A');
        expect(plant.notes, 'Auto-flowering plant');
        expect(plant.seedBank, 'Sensi Seeds');
        expect(plant.breeder, 'Sensi Seeds');
        expect(plant.status, 'flowering');
      });

      test('should calculate plant age correctly', () {
        final plantedDate = DateTime(2024, 1, 1);
        final plant = Plant(
          id: 1,
          name: 'Test Plant',
          cultivarName: 'Test',
          strain: 'Test',
          plantedDate: plantedDate,
          createdAt: plantedDate,
          updatedAt: plantedDate,
          location: 'Test',
          notes: 'Test',
          seedBank: 'Test',
          breeder: 'Test',
          status: 'active',
        );

        final now = DateTime.now();
        final expectedAge = now.difference(plantedDate).inDays;

        expect(plant.ageInDays, expectedAge);
      });

      test('should provide correct cultivar display name', () {
        final plant1 = Plant(
          id: 1,
          name: 'Test Plant',
          cultivarName: 'Northern Lights',
          strain: 'Indica',
          plantedDate: DateTime(2024, 1, 1),
          createdAt: DateTime(2024, 1, 1),
          updatedAt: DateTime(2024, 1, 1),
          location: 'Test',
          notes: 'Test',
          seedBank: 'Test',
          breeder: 'Test',
          status: 'active',
        );

        final plant2 = Plant(
          id: 2,
          name: 'Test Plant 2',
          cultivarName: null,
          strain: 'White Widow',
          plantedDate: DateTime(2024, 1, 1),
          createdAt: DateTime(2024, 1, 1),
          updatedAt: DateTime(2024, 1, 1),
          location: 'Test',
          notes: 'Test',
          seedBank: 'Test',
          breeder: 'Test',
          status: 'active',
        );

        expect(
            plant1.cultivarDisplay, 'Northern Lights'); // prefers cultivarName
        expect(plant2.cultivarDisplay, 'White Widow'); // falls back to strain
      });

      test('should provide correct status display names', () {
        final statusTests = [
          {'input': 'seedling', 'expected': '🌱 Seedling'},
          {'input': 'vegetative', 'expected': '🌿 Growing'},
          {'input': 'flowering', 'expected': '🌸 Flowering'},
          {'input': 'harvested', 'expected': '✂️ Harvested'},
          {'input': 'dried', 'expected': '🪣 Dried'},
          {'input': 'cured', 'expected': '🏺 Cured'},
          {'input': 'unknown', 'expected': 'unknown'},
        ];

        for (final testCase in statusTests) {
          final plant = Plant(
            id: 1,
            name: 'Test Plant',
            cultivarName: 'Test',
            strain: 'Test',
            plantedDate: DateTime(2024, 1, 1),
            createdAt: DateTime(2024, 1, 1),
            updatedAt: DateTime(2024, 1, 1),
            location: 'Test',
            notes: 'Test',
            seedBank: 'Test',
            breeder: 'Test',
            status: testCase['input'] as String,
          );

          expect(plant.statusDisplay, testCase['expected']);
        }
      });

      test('should provide correct string representation', () {
        final plant = Plant(
          id: 1,
          name: 'Northern Lights #5',
          cultivarName: 'Northern Lights',
          strain: 'Indica',
          plantedDate: DateTime(2024, 1, 1),
          createdAt: DateTime(2024, 1, 1),
          updatedAt: DateTime(2024, 1, 1),
          location: 'Grow Room A',
          notes: 'Auto-flowering plant',
          seedBank: 'Sensi Seeds',
          breeder: 'Sensi Seeds',
          status: 'flowering',
        );

        expect(plant.toString(),
            'Plant{id: 1, name: Northern Lights #5, cultivarName: Northern Lights, status: flowering}');
      });
    });

    // Breeder Model Tests
    group('Breeder Models', () {
      test('should create valid Breeder model', () {
        final breeder = Breeder(
          id: 123,
          name: 'Sensi Seeds',
        );

        expect(breeder.id, 123);
        expect(breeder.name, 'Sensi Seeds');
      });

      test('should create Breeder from JSON', () {
        final json = {
          'id': 123,
          'name': 'Sensi Seeds',
        };

        final breeder = Breeder.fromJson(json);

        expect(breeder.id, 123);
        expect(breeder.name, 'Sensi Seeds');
      });

      test('should convert Breeder to JSON', () {
        final breeder = Breeder(
          id: 123,
          name: 'Sensi Seeds',
        );

        final json = breeder.toJson();

        expect(json['id'], 123);
        expect(json['name'], 'Sensi Seeds');
      });

      test('should compare Breeder objects correctly', () {
        final breeder1 = Breeder(
          id: 123,
          name: 'Sensi Seeds',
        );

        final breeder2 = Breeder(
          id: 123,
          name: 'Sensi Seeds',
        );

        final breeder3 = Breeder(
          id: 456,
          name: 'Dutch Passion',
        );

        expect(breeder1 == breeder2, true); // same ID
        expect(breeder1 == breeder3, false); // different ID
      });
    });

    // CultivarStats Model Tests
    group('CultivarStats Models', () {
      test('should create valid CultivarStats model', () {
        final stats = CultivarStats(
          totalCultivars: 15,
          autoflower: 8,
          photoperiod: 7,
          mostUsedCultivar: 'Northern Lights',
          mostUsedCount: 5,
        );

        expect(stats.totalCultivars, 15);
        expect(stats.autoflower, 8);
        expect(stats.photoperiod, 7);
        expect(stats.mostUsedCultivar, 'Northern Lights');
        expect(stats.mostUsedCount, 5);
      });

      test('should create CultivarStats from JSON', () {
        final json = {
          'total_cultivars': 15,
          'autoflower': 8,
          'photoperiod': 7,
          'most_used_cultivar': 'Northern Lights',
          'most_used_count': 5,
        };

        final stats = CultivarStats.fromJson(json);

        expect(stats.totalCultivars, 15);
        expect(stats.autoflower, 8);
        expect(stats.photoperiod, 7);
        expect(stats.mostUsedCultivar, 'Northern Lights');
        expect(stats.mostUsedCount, 5);
      });

      test('should convert CultivarStats to JSON', () {
        final stats = CultivarStats(
          totalCultivars: 15,
          autoflower: 8,
          photoperiod: 7,
          mostUsedCultivar: 'Northern Lights',
          mostUsedCount: 5,
        );

        final json = stats.toJson();

        expect(json['total_cultivars'], 15);
        expect(json['autoflower'], 8);
        expect(json['photoperiod'], 7);
        expect(json['most_used_cultivar'], 'Northern Lights');
        expect(json['most_used_count'], 5);
      });
    });
  });
}
