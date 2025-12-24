// Unit Tests for Core Models - Comprehensive model validation
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/features/plants/domain/plant.dart';
import 'package:cultivar_app/core/models/cultivar_models.dart';
import 'package:cultivar_app/core/models/create_plant_request.dart';

void main() {
  group('Model Tests', () {
    // Cultivar Models Tests
    group('Cultivar Models', () {
      test('should create valid Cultivar model with required fields', () {
        final cultivar = Cultivar(
          id: 1,
          name: 'Northern Lights',
          description: 'Classic indica',
          genetics: 'Indica',
          thcContent: 18.0,
          cbdContent: 1.0,
          effects: 'Relaxing',
          flavor: 'Sweet',
          breederId: 1,
          isActive: true,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        expect(cultivar.id, 1);
        expect(cultivar.name, 'Northern Lights');
        expect(cultivar.genetics, 'Indica');
        expect(cultivar.thcContent, 18.0);
      });

      test('should create Cultivar from JSON', () {
        final json = {
          'id': 123,
          'name': 'Northern Lights',
          'description': 'Classic indica strain',
          'genetics': 'Indica',
          'thc_content': 18.0,
          'cbd_content': 1.0,
          'effects': 'Relaxing',
          'flavor': 'Sweet',
          'breeder_id': 456,
          'is_active': true,
          'created_at': '2024-01-01T00:00:00.000',
          'updated_at': '2024-01-01T00:00:00.000',
        };

        final cultivar = Cultivar.fromJson(json);

        expect(cultivar.id, 123);
        expect(cultivar.name, 'Northern Lights');
        expect(cultivar.breederId, 456);
        expect(cultivar.genetics, 'Indica');
      });
    });

    // Plant Models Tests
    group('Plant Models', () {
      test('should create valid CreatePlantRequest model', () {
        final createRequest = CreatePlantRequest(
          name: 'White Widow',
          cultivar: 'Northern Lights',
          plantingDate: DateTime(2024, 1, 15),
          zone: 'Grow Room A',
          notes: 'First planting',
        );

        expect(createRequest.name, 'White Widow');
        expect(createRequest.cultivar, 'Northern Lights');
        expect(createRequest.plantingDate, DateTime(2024, 1, 15));
        expect(createRequest.zone, 'Grow Room A');
        expect(createRequest.notes, 'First planting');
      });

      test('should create valid Plant model', () {
        final plant = Plant(
          id: '1',
          name: 'Northern Lights #5',
          stage: PlantStage.flowering,
          status: PlantStatus.active,
          health: PlantHealth.healthy,
          plantedDate: DateTime(2024, 1, 1),
          strain: 'Indica',
          notes: 'Auto-flowering plant',
        );

        expect(plant.id, '1');
        expect(plant.name, 'Northern Lights #5');
        expect(plant.stage, PlantStage.flowering);
        expect(plant.status, PlantStatus.active);
        expect(plant.health, PlantHealth.healthy);
        expect(plant.plantedDate, DateTime(2024, 1, 1));
        expect(plant.strain, 'Indica');
        expect(plant.notes, 'Auto-flowering plant');
      });

      test('should provide correct status display names', () {
        expect(PlantStage.seedling.displayName, 'Seedling');
        expect(PlantStage.vegetative.displayName, 'Vegetative');
        expect(PlantStage.flowering.displayName, 'Flowering');
        expect(PlantStage.harvest.displayName, 'Harvest');
      });
    });

    // Breeder Model Tests
    group('Breeder Models', () {
      test('should create valid Breeder model', () {
        final breeder = Breeder(
          id: 123,
          name: 'Sensi Seeds',
          description: 'Famous breeder',
          website: 'https://sensiseeds.com',
          isActive: true,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        expect(breeder.id, 123);
        expect(breeder.name, 'Sensi Seeds');
      });
    });

    // CultivarStats Model Tests
    group('CultivarStats Models', () {
      test('should create valid CultivarStats model', () {
        final stats = const CultivarStats(
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
    });
  });
}
