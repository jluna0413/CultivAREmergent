import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import 'package:cultivar_app/features/dashboard/data/dashboard_api_client.dart';
import 'package:cultivar_app/features/dashboard/domain/dashboard_stats_model.dart';

@GenerateMocks([ApiClient])
import 'dashboard_api_client_test.mocks.dart';

void main() {
  late MockApiClient mockApiClient;
  late DashboardApiClient dashboardApiClient;

  setUp(() {
    mockApiClient = MockApiClient();
    dashboardApiClient = DashboardApiClient(mockApiClient);
  });

  group('DashboardApiClient', () {
    test('getDashboardStats calls correct endpoint', () async {
      // Arrange
      final mockResponse = {
        'counts': {
          'total': 10,
          'active': 8,
          'harvested': 2,
          'seedlings': 3,
          'vegetative': 3,
          'flowering': 2,
        },
        'cultivars': {'total_cultivars': 15, 'user_cultivars': 5},
        'environment': {
          'avg_temperature': 22.5,
          'avg_humidity': 65.0,
          'avg_ph': 6.2,
          'avg_ec': 1.8,
        },
        'sensors': {
          'total_sensors': 4,
          'active_sensors': 3,
          'last_reading_time': '2025-12-07T02:00:00Z',
        },
        'data_slices': {
          'temperature_data': [],
          'humidity_data': [],
          'ph_data': [],
          'ec_data': [],
        },
        'recent_readings': [
          {
            'timestamp': '2025-12-07T02:00:00Z',
            'sensor_type': 'temperature',
            'value': 22.5,
            'unit': '°C',
            'location': 'grow_room_1',
          },
        ],
        'recent_activities': [
          {
            'timestamp': '2025-12-07T02:00:00Z',
            'activity_type': 'watering',
            'description': 'Watered plant #123',
            'plant_id': 123,
            'severity': 'normal',
          },
        ],
        'generated_at': '2025-12-07T02:00:00Z',
        'user_id': 1,
      };

      when(
        mockApiClient.get(
          '/api/v2/dashboard/stats',
          queryParameters: anyNamed('queryParameters'),
        ),
      ).thenAnswer((_) async => mockResponse);

      // Act
      final result = await dashboardApiClient.getDashboardStats();

      // Assert
      expect(result, isA<DashboardStats>());
      expect(result.counts.total, equals(10));
      expect(result.counts.active, equals(8));
      expect(result.cultivars.userCultivars, equals(5));

      verify(
        mockApiClient.get(
          '/api/v2/dashboard/stats',
          queryParameters: anyNamed('queryParameters'),
        ),
      ).called(1);
    });

    test('getDashboardStats handles API errors', () async {
      // Arrange
      when(
        mockApiClient.get(
          '/api/v2/dashboard/stats',
          queryParameters: anyNamed('queryParameters'),
        ),
      ).thenThrow(Exception('Network error'));

      // Act & Assert
      expect(
        () => dashboardApiClient.getDashboardStats(),
        throwsA(isA<Exception>()),
      );
    });
  });
}
