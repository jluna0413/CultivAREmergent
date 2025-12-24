import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/features/dashboard/domain/dashboard_stats_model.dart';

void main() {
  group('DashboardStats', () {
    test('should create DashboardStats with all required fields', () {
      final stats = DashboardStats(
        counts: const CountStats(
          total: 10,
          active: 5,
          harvested: 2,
          seedlings: 3,
          vegetative: 3,
          flowering: 2,
        ),
        cultivars: const CultivarStats(totalCultivars: 8, userCultivars: 5),
        environment: const EnvironmentalStats(
          avgTemperature: 24.5,
          avgHumidity: 65.0,
          avgPh: 6.2,
          avgEc: 1.8,
        ),
        sensors: const SensorStats(totalSensors: 12, activeSensors: 11),
        dataSlices: const EnvironmentalSlice(
          temperatureData: [],
          humidityData: [],
          phData: [],
          ecData: [],
        ),
        growthPhases: [
          const GrowthPhaseSlice(name: 'Seedling', count: 3, percentage: 30.0),
        ],
        recentReadings: [
          RecentReading(
            timestamp: DateTime.now(),
            sensorType: 'Temperature',
            value: 24.5,
            unit: '°C',
          ),
        ],
        recentActivities: [
          RecentActivity(
            timestamp: DateTime.now(),
            activityType: 'Watering',
            description: 'Watered Plant #1',
            plantId: 1,
            severity: 'Info',
          ),
        ],
        userId: 1,
        generatedAt: DateTime.now(),
      );

      expect(stats.counts.total, equals(10));
      expect(stats.counts.active, equals(5));
      expect(stats.cultivars.totalCultivars, equals(8));
      expect(stats.environment.avgTemperature, equals(24.5));
      expect(stats.userId, equals(1));
    });

    // test('should serialize to JSON correctly', () {
    //   final stats = DashboardStats(
    //     counts: const CountStats(
    //       total: 10,
    //       active: 5,
    //       harvested: 2,
    //       seedlings: 3,
    //       vegetative: 3,
    //       flowering: 2,
    //     ),
    //     cultivars: const CultivarStats(totalCultivars: 8, userCultivars: 5),
    //     environment: const EnvironmentalStats(
    //       avgTemperature: 24.5,
    //       avgHumidity: 65.0,
    //       avgPh: 6.2,
    //       avgEc: 1.8,
    //     ),
    //     sensors: const SensorStats(totalSensors: 12, activeSensors: 11),
    //     dataSlices: const EnvironmentalSlice(
    //       temperatureData: [],
    //       humidityData: [],
    //       phData: [],
    //       ecData: [],
    //     ),
    //     growthPhases: [],
    //     recentReadings: [],
    //     recentActivities: [],
    //     userId: 1,
    //     generatedAt: DateTime.now(),
    //   );

    //   final json = stats.toJson();

    //   expect(json, isA<Map<String, dynamic>>());
    //   expect(json['counts'], isA<Map<String, dynamic>>());
    //   expect(json['cultivars'], isA<Map<String, dynamic>>());
    //   expect(json['environment'], isA<Map<String, dynamic>>());
    //   expect(json['user_id'], equals(1));
    // });

    test('should deserialize from JSON correctly', () {
      final json = {
        'counts': {
          'total': 10,
          'active': 5,
          'harvested': 2,
          'seedlings': 3,
          'vegetative': 3,
          'flowering': 2,
        },
        'cultivars': {'total_cultivars': 8, 'user_cultivars': 5},
        'environment': {
          'avg_temperature': 24.5,
          'avg_humidity': 65.0,
          'avg_ph': 6.2,
          'avg_ec': 1.8,
        },
        'sensors': {'total_sensors': 12, 'active_sensors': 11},
        'data_slices': {
          'temperature_data': [],
          'humidity_data': [],
          'ph_data': [],
          'ec_data': [],
        },
        'growth_phases': [],
        'recent_readings': [],
        'recent_activities': [],
        'generated_at': DateTime.now().toIso8601String(),
        'user_id': 1,
      };

      final stats = DashboardStats.fromJson(json);

      expect(stats.counts.total, equals(10));
      expect(stats.cultivars.totalCultivars, equals(8));
      expect(stats.environment.avgTemperature, equals(24.5));
      expect(stats.userId, equals(1));
    });

    test('should calculate growth phase percentages correctly', () {
      final growthPhases = [
        const GrowthPhaseSlice(phase: 'Seedling', count: 3, percentage: 30.0),
        const GrowthPhaseSlice(name: 'Vegetative', count: 4, percentage: 40.0),
        const GrowthPhaseSlice(name: 'Flowering', count: 3, percentage: 30.0),
      ];

      final total = growthPhases.fold<int>(
        0,
        (sum, phase) => sum + phase.count,
      );
      expect(total, equals(10));

      final totalPercentage = growthPhases.fold<double>(
        0.0,
        (sum, phase) => sum + phase.percentage,
      );
      expect(totalPercentage, equals(100.0));
    });

    test('should support legacy getters for backwards compatibility', () {
      final stats = DashboardStats(
        counts: const CountStats(
          total: 10,
          active: 5,
          harvested: 2,
          seedlings: 3,
          vegetative: 3,
          flowering: 2,
        ),
        cultivars: const CultivarStats(totalCultivars: 8, userCultivars: 5),
        environment: const EnvironmentalStats(
          avgTemperature: 24.5,
          avgHumidity: 65.0,
        ),
        sensors: const SensorStats(totalSensors: 12, activeSensors: 11),
        dataSlices: const EnvironmentalSlice(
          temperatureData: [],
          humidityData: [],
          phData: [],
          ecData: [],
        ),
        growthPhases: [],
        userId: 1,
        generatedAt: DateTime.now(),
      );

      // Test legacy getters
      expect(stats.totalPlants, equals(10));
      expect(stats.activePlants, equals(5));
      expect(stats.totalStrains, equals(8));
      expect(stats.harvested, equals(2));
    });
  });

  group('CountStats', () {
    test('should create CountStats with all fields', () {
      final counts = const CountStats(
        total: 15,
        active: 8,
        harvested: 3,
        seedlings: 4,
        vegetative: 5,
        flowering: 3,
      );

      expect(counts.total, equals(15));
      expect(counts.active, equals(8));
      expect(counts.harvested, equals(3));
    });
  });

  group('EnvironmentalStats', () {
    test('should create EnvironmentalStats with valid ranges', () {
      final env = const EnvironmentalStats(
        avgTemperature: 23.5,
        avgHumidity: 68.2,
        avgPh: 6.1,
        avgEc: 1.9,
      );

      expect(env.avgTemperature, inInclusiveRange(18, 30));
      expect(env.avgHumidity, inInclusiveRange(40, 80));
      expect(env.avgPh, inInclusiveRange(5.5, 7.5));
      expect(env.avgEc, inInclusiveRange(1.0, 3.0));
    });

    test('should handle nullable pH and EC values', () {
      final env = const EnvironmentalStats(
        avgTemperature: 24.0,
        avgHumidity: 60.0,
      );

      expect(env.avgPh, isNull);
      expect(env.avgEc, isNull);
    });
  });

  group('GrowthPhaseSlice', () {
    test('should create GrowthPhaseSlice with correct calculations', () {
      final slice = const GrowthPhaseSlice(
        name: 'Flowering',
        count: 3,
        percentage: 30.0,
      );

      expect(slice.name, equals('Flowering'));
      expect(slice.count, equals(3));
      expect(slice.percentage, equals(30.0));
    });
  });

  group('RecentReading', () {
    test('should create RecentReading with all required fields', () {
      final timestamp = DateTime.now();
      final reading = RecentReading(
        timestamp: timestamp,
        sensorType: 'Humidity',
        value: 65.0,
        unit: '%',
        location: 'Grow Room A',
      );

      expect(reading.sensorType, equals('Humidity'));
      expect(reading.value, equals(65.0));
      expect(reading.unit, equals('%'));
      expect(reading.location, equals('Grow Room A'));
    });
  });

  group('RecentActivity', () {
    test('should create RecentActivity with all required fields', () {
      final timestamp = DateTime.now();
      final activity = RecentActivity(
        timestamp: timestamp,
        activityType: 'Feeding',
        description: 'Added nutrients to Plant #2',
        plantId: 2,
        severity: 'Success',
      );

      expect(activity.activityType, equals('Feeding'));
      expect(activity.description, equals('Added nutrients to Plant #2'));
      expect(activity.plantId, equals(2));
      expect(activity.severity, equals('Success'));
    });
  });
}
