# CultivAR Flutter Testing Guide

## Table of Contents
1. [Testing Strategy Overview](#testing-strategy-overview)
2. [Testing Pyramid](#testing-pyramid)
3. [Unit Tests](#unit-tests)
4. [Widget Tests](#widget-tests)
5. [Integration Tests](#integration-tests)
6. [Mocking and Test Fixtures](#mocking-and-test-fixtures)
7. [Riverpod Provider Testing](#riverpod-provider-testing)
8. [API Testing](#api-testing)
9. [Error Handling and Edge Cases](#error-handling-and-edge-cases)
10. [Test Coverage Goals](#test-coverage-goals)
11. [Continuous Integration](#continuous-integration)
12. [Best Practices](#best-practices)

## Testing Strategy Overview

The CultivAR Flutter application follows a comprehensive testing strategy with **80% minimum code coverage** requirement. Our testing approach emphasizes:

- **Fast feedback loops** through automated testing
- **Reliable test suites** that catch regressions early
- **Maintainable test code** following DRY principles
- **Real-world scenario testing** including error conditions
- **Performance and accessibility testing**

### Testing Philosophy

```
Code Test Coverage Priority:
├── Business Logic (Unit Tests): 90%+
├── UI Components (Widget Tests): 80%+
├── API Integration (Integration Tests): 75%+
└── Critical User Flows (E2E Tests): 100%
```

## Testing Pyramid

We follow the testing pyramid approach with clear separation of concerns:

```
         ┌─────────────────┐
         │   E2E Tests     │ ← Top: Few, Critical Path
         │   (Slow)        │
         └─────────────────┘
       ┌─────────────────────┐
       │ Integration Tests   │ ← Middle: Some, Feature Flow
       │   (Medium)         │
       └─────────────────────┘
     ┌───────────────────────────┐
     │ Widget Tests              │ ← Bottom: Many, UI Components
     │   (Fast)                  │
     └───────────────────────────┘
   ┌───────────────────────────────┐
   │ Unit Tests                    │ ← Foundation: Most, Logic
   │   (Very Fast)                 │
   └───────────────────────────────┘
```

## Unit Tests

### Location & Structure
```dart
// Location: test/unit/
├── models/
│   ├── user_model_test.dart
│   ├── plant_model_test.dart
│   └── dashboard_stats_test.dart
├── services/
│   ├── auth_service_test.dart
│   └── api_client_test.dart
├── utils/
│   ├── validation_test.dart
│   └── formatters_test.dart
└── providers/
    ├── auth_provider_test.dart
    └── dashboard_provider_test.dart
```

### Unit Test Examples

#### Model Testing with Freezed
```dart
// test/unit/models/plant_model_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:cultivar_app/features/plants/domain/plant_model.dart';

@GenerateMocks([PlantRepository])
import 'plant_model_test.mocks.dart';

void main() {
  group('Plant Model Tests', () {
    test('should create plant from JSON', () {
      // Arrange
      final json = {
        'id': 1,
        'name': 'Test Plant',
        'statusId': 2,
        'currentDay': 30,
        'strainUrl': 'https://example.com/strain',
        'createdAt': '2023-01-01T00:00:00Z',
        'updatedAt': '2023-01-01T00:00:00Z',
      };

      // Act
      final plant = Plant.fromJson(json);

      // Assert
      expect(plant.id, equals(1));
      expect(plant.name, equals('Test Plant'));
      expect(plant.currentDay, equals(30));
    });

    test('should copy plant with updated fields', () {
      // Arrange
      final originalPlant = Plant(
        id: 1,
        name: 'Original Plant',
        statusId: 1,
        currentDay: 25,
        startDt: DateTime(2023, 1, 1),
        createdAt: DateTime(2023, 1, 1),
        updatedAt: DateTime(2023, 1, 1),
      );

      // Act
      final updatedPlant = originalPlant.copyWith(
        name: 'Updated Plant',
        currentDay: 26,
      );

      // Assert
      expect(updatedPlant.name, equals('Updated Plant'));
      expect(updatedPlant.currentDay, equals(26));
      expect(updatedPlant.id, equals(1)); // Unchanged
      expect(updatedPlant.statusId, equals(1)); // Unchanged
    });

    test('should validate required fields', () {
      // Arrange
      final invalidJson = {
        'id': null, // Required field
        'name': null, // Required field
        'statusId': 1,
        'currentDay': 30,
      };

      // Act & Assert
      expect(
        () => Plant.fromJson(invalidJson),
        throwsA(isA<Exception>()),
      );
    });
  });
}
```

#### Service Layer Testing with Mockito
```dart
// test/unit/services/auth_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:cultivar_app/core/services/auth_service.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import 'auth_service_test.mocks.dart';

@GenerateMocks([ApiClient])
import 'auth_service_test.mocks.dart';

void main() {
  group('AuthService Tests', () {
    late AuthService authService;
    late MockApiClient mockApiClient;

    setUp(() {
      mockApiClient = MockApiClient();
      authService = AuthService(apiClient: mockApiClient);
    });

    test('should login successfully with valid credentials', () async {
      // Arrange
      final loginRequest = LoginRequest(
        email: 'test@example.com',
        password: 'password123',
      );

      final mockResponse = {
        'token': 'fake-jwt-token',
        'user': {
          'id': 1,
          'email': 'test@example.com',
          'username': 'testuser',
        },
      };

      when(mockApiClient.post('/auth/login', data: loginRequest.toJson()))
          .thenAnswer((_) async => mockResponse);

      // Act
      final result = await authService.login(loginRequest);

      // Assert
      expect(result.token, equals('fake-jwt-token'));
      expect(result.user.email, equals('test@example.com'));
      verify(mockApiClient.post('/auth/login', data: loginRequest.toJson())).called(1);
    });

    test('should throw AuthException for invalid credentials', () async {
      // Arrange
      final loginRequest = LoginRequest(
        email: 'test@example.com',
        password: 'wrongpassword',
      );

      when(mockApiClient.post('/auth/login', data: anyNamed('data')))
          .thenThrow(AuthException('Invalid credentials'));

      // Act & Assert
      expect(
        () => authService.login(loginRequest),
        throwsA(isA<AuthException>()),
      );
    });

    test('should handle network timeout gracefully', () async {
      // Arrange
      final loginRequest = LoginRequest(
        email: 'test@example.com',
        password: 'password123',
      );

      when(mockApiClient.post('/auth/login', data: anyNamed('data')))
          .thenThrow(TimeoutException('Request timeout'));

      // Act & Assert
      expect(
        () => authService.login(loginRequest),
        throwsA(isA<TimeoutException>()),
      );
    });
  });
}
```

## Widget Tests

### Location & Structure
```dart
// Location: test/widget/
├── widgets/
│   ├── plant_card_test.dart
│   ├── stat_card_test.dart
│   └── glass_card_test.dart
├── screens/
│   ├── login_screen_test.dart
│   ├── dashboard_screen_test.dart
│   └── plants_list_screen_test.dart
└── forms/
    ├── plant_form_test.dart
    └── settings_form_test.dart
```

### Widget Test Examples

#### Component Testing
```dart
// test/widget/widgets/plant_card_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:cultivar_app/core/widgets/plant_card.dart';
import 'package:cultivar_app/features/plants/domain/plant_model.dart';

void main() {
  group('PlantCard Widget Tests', () {
    final testPlant = Plant(
      id: 1,
      name: 'Test Plant',
      statusId: 2,
      currentDay: 30,
      strainUrl: 'https://example.com/strain',
      startDt: DateTime(2023, 1, 1),
      createdAt: DateTime(2023, 1, 1),
      updatedAt: DateTime(2023, 1, 1),
    );

    testWidgets('should display plant information correctly', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PlantCard(
              plant: testPlant,
              onTap: () {},
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('Test Plant'), findsOneWidget);
      expect(find.text('Day 30'), findsOneWidget);
      expect(find.byType(GestureDetector), findsOneWidget);
    });

    testWidgets('should call onTap when tapped', (WidgetTester tester) async {
      // Arrange
      bool isTapped = false;
      final onTap = () => isTapped = true;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PlantCard(
              plant: testPlant,
              onTap: onTap,
            ),
          ),
        ),
      );

      // Act
      await tester.tap(find.byType(GestureDetector));
      await tester.pumpAndSettle();

      // Assert
      expect(isTapped, isTrue);
    });

    testWidgets('should show loading state when plant is null', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PlantCard(
              plant: null,
              onTap: () {},
              isLoading: true,
            ),
          ),
        ),
      );

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
      expect(find.text('Loading...'), findsOneWidget);
    });

    testWidgets('should show error state when data is invalid', (WidgetTester tester) async {
      // Arrange
      final invalidPlant = testPlant.copyWith(name: null);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: PlantCard(
              plant: invalidPlant,
              onTap: () {},
            ),
          ),
        ),
      );

      // Assert
      expect(find.text('Unknown Plant'), findsOneWidget);
      expect(find.byType(Icon), findsOneWidget);
    });
  });
}
```

#### Screen Testing with Riverpod
```dart
// test/widget/screens/login_screen_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:provider/provider.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cultivar_app/features/auth/screens/login_screen.dart';
import 'package:cultivar_app/core/state/auth_provider.dart';

void main() {
  group('LoginScreen Widget Tests', () {
    testWidgets('should render login form correctly', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Assert
      expect(find.text('CultivAR'), findsOneWidget);
      expect(find.byType(TextFormField), findsNWidgets(2));
      expect(find.byKey(const Key('emailField')), findsOneWidget);
      expect(find.byKey(const Key('passwordField')), findsOneWidget);
      expect(find.byKey(const Key('loginButton')), findsOneWidget);
      expect(find.text('Sign In'), findsOneWidget);
    });

    testWidgets('should show validation errors for empty fields', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Act - Try to login without entering any data
      await tester.tap(find.byKey(const Key('loginButton')));
      await tester.pumpAndSettle();

      // Assert
      expect(find.text('Please enter your email'), findsOneWidget);
      expect(find.text('Please enter your password'), findsOneWidget);
      expect(find.byType(LoginScreen), findsOneWidget); // Still on login screen
    });

    testWidgets('should validate email format', (WidgetTester tester) async {
      // Arrange
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Act - Enter invalid email
      await tester.enterText(
        find.byKey(const Key('emailField')),
        'invalid-email',
      );
      await tester.tap(find.byKey(const Key('loginButton')));
      await tester.pumpAndSettle();

      // Assert
      expect(find.text('Please enter a valid email'), findsOneWidget);
    });

    testWidgets('should handle loading state during login', (WidgetTester tester) async {
      // Arrange
      final container = ProviderScope(
        child: MaterialApp(
          home: const LoginScreen(),
        ),
      );

      await tester.pumpWidget(container);

      // Act - Enter valid credentials and tap login
      await tester.enterText(
        find.byKey(const Key('emailField')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(const Key('passwordField')),
        'password123',
      );
      await tester.tap(find.byKey(const Key('loginButton')));
      await tester.pumpAndSettle();

      // Assert - Check for loading indicator or button state change
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });
  });
}
```

## Integration Tests

### Location & Structure
```dart
// Location: integration_test/
├── auth_flow_test.dart           // Complete authentication flow
├── dashboard_flow_test.dart      // Dashboard functionality
├── plants_management_test.dart   // Plant CRUD operations
└── app_test.dart                // Core app functionality
```

### Integration Test Examples

#### Complete Auth Flow
```dart
// integration_test/auth_flow_test.dart (previously created and enhanced)
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:cultivar_app/main.dart' as app;
import 'package:cultivar_app/features/auth/screens/login_screen.dart';
import 'package:cultivar_app/features/dashboard/ui/dashboard_screen.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Auth Flow Integration Tests', () {
    testWidgets('should show login screen on startup',
        (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Expect to be on the login screen
      expect(find.byType(LoginScreen), findsOneWidget);
      expect(find.text('CultivAR'), findsOneWidget);

      // Verify login form elements are present
      expect(
          find.byType(TextFormField), findsNWidgets(2)); // username + password
      expect(find.text('Sign In'), findsOneWidget);
    });

    testWidgets('should login and navigate to dashboard successfully',
        (WidgetTester tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Find form fields by semantic labels or hint text
      final usernameField = find.byKey(const Key('usernameField'));
      final passwordField = find.byKey(const Key('passwordField'));

      // Fallback to find by type if keys not available
      final allTextFields = find.byType(TextFormField);

      await tester.enterText(usernameField, 'testuser@example.com');
      await tester.enterText(passwordField, 'password123');
      await tester.pumpAndSettle();

      // Find and tap the login button
      final loginButton = find.byKey(const Key('loginButton'));
      await tester.tap(loginButton);

      // Wait for navigation and any loading states
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Verify navigation to dashboard
      expect(find.byType(DashboardScreen), findsOneWidget);

      // Verify dashboard content
      expect(find.text('Dashboard'), findsOneWidget);
      expect(find.byKey(const Key('logoutButton')), findsOneWidget);
    });
  });
}
```

#### Plants Management Flow
```dart
// integration_test/plants_management_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:cultivar_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Plants Management Integration Tests', () {
    testWidgets('complete plant management flow', (WidgetTester tester) async {
      // Arrange - Start authenticated app
      app.main();
      await tester.pumpAndSettle();

      // Login first
      final emailField = find.byKey(const Key('emailField'));
      final passwordField = find.byKey(const Key('passwordField'));
      final loginButton = find.byKey(const Key('loginButton'));

      await tester.enterText(emailField, 'test@example.com');
      await tester.enterText(passwordField, 'password123');
      await tester.tap(loginButton);
      await tester.pumpAndSettle(const Duration(seconds: 3));

      // Navigate to plants screen
      final plantsTab = find.byKey(const Key('plantsTab'));
      await tester.tap(plantsTab);
      await tester.pumpAndSettle();

      // Verify plants list is loaded
      expect(find.byKey(const Key('plantsList')), findsOneWidget);
      expect(find.byType(ListView), findsOneWidget);

      // Add new plant
      final addButton = find.byKey(const Key('addPlantButton'));
      await tester.tap(addButton);
      await tester.pumpAndSettle();

      // Fill plant form
      final nameField = find.byKey(const Key('plantNameField'));
      final strainDropdown = find.byKey(const Key('strainDropdown'));
      final saveButton = find.byKey(const Key('savePlantButton'));

      await tester.enterText(nameField, 'Test Plant');
      await tester.tap(strainDropdown);
      await tester.pumpAndSettle();

      // Select first strain
      await tester.tap(find.text('White Widow').first);
      await tester.pumpAndSettle();

      // Save plant
      await tester.tap(saveButton);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify plant was added to list
      expect(find.text('Test Plant'), findsOneWidget);

      // Edit plant
      final plantCard = find.text('Test Plant');
      await tester.tap(plantCard);
      await tester.pumpAndSettle();

      // Update plant name
      final editButton = find.byKey(const Key('editPlantButton'));
      await tester.tap(editButton);
      await tester.pumpAndSettle();

      final updatedNameField = find.byKey(const Key('plantNameField'));
      await tester.clearAndEnterText(updatedNameField, 'Updated Plant');
      
      final updateButton = find.byKey(const Key('updatePlantButton'));
      await tester.tap(updateButton);
      await tester.pumpAndSettle(const Duration(seconds: 2));

      // Verify plant was updated
      expect(find.text('Updated Plant'), findsOneWidget);
      expect(find.text('Test Plant'), findsNothing);
    });
  });
}
```

## Mocking and Test Fixtures

### Test Fixtures
```dart
// test/utils/test_fixtures.dart
import 'package:cultivar_app/features/plants/domain/plant_model.dart';
import 'package:cultivar_app/features/auth/domain/user_model.dart';
import 'package:cultivar_app/core/models/dashboard_stats.dart';

class TestFixtures {
  // Plant fixtures
  static Plant get testPlant => Plant(
    id: 1,
    name: 'Test Plant',
    statusId: 1,
    currentDay: 30,
    currentWeek: 4,
    startDt: DateTime(2023, 1, 1),
    createdAt: DateTime(2023, 1, 1),
    updatedAt: DateTime(2023, 1, 1),
  );

  static Plant get invalidPlant => Plant(
    id: null, // Invalid
    name: null, // Invalid
    statusId: 1,
    currentDay: 30,
    startDt: DateTime(2023, 1, 1),
    createdAt: DateTime(2023, 1, 1),
    updatedAt: DateTime(2023, 1, 1),
  );

  // User fixtures
  static User get testUser => User(
    id: 1,
    username: 'testuser',
    email: 'test@example.com',
    isAdmin: false,
  );

  // Dashboard stats fixtures
  static DashboardStats get testDashboardStats => DashboardStats(
    totalPlants: 42,
    activePlants: 35,
    completedCycles: 7,
    averageYield: 125.5,
  );
}
```

### Mock Generators
```dart
// test/mocks/mock_providers.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/annotations.dart';
import 'package:cultivar_app/core/services/api_client.dart';
import 'package:cultivar_app/features/plants/domain/plant_repository.dart';
import 'mock_providers.mocks.dart';

// Generate mocks for external dependencies
@GenerateMocks([ApiClient, PlantRepository])
import 'mock_providers.mocks.dart';

// Provider overrides for testing
final mockPlantsProvider = Provider<List<Plant>>((ref) {
  return [TestFixtures.testPlant];
});

final mockDashboardStatsProvider = FutureProvider<DashboardStats>((ref) {
  return Future.value(TestFixtures.testDashboardStats);
});

// HTTP client mocks
class MockHttpClient extends Mock implements ApiClient {}
```

## Riverpod Provider Testing

### Provider Testing Best Practices
```dart
// test/unit/providers/dashboard_provider_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/annotations.dart';
import 'package:cultivar_app/core/state/dashboard_provider.dart';
import 'package:cultivar_app/core/services/api_client.dart';
import 'dashboard_provider_test.mocks.dart';

@GenerateMocks([ApiClient])
import 'dashboard_provider_test.mocks.dart';

void main() {
  group('Dashboard Provider Tests', () {
    late ProviderContainer container;
    late MockApiClient mockApiClient;

    setUp(() {
      mockApiClient = MockApiClient();
      container = ProviderContainer(
        overrides: [
          apiClientProvider.overrideWithValue(mockApiClient),
        ],
      );
    });

    tearDown(() {
      container.dispose();
    });

    test('should load dashboard stats successfully', () async {
      // Arrange
      final mockStats = DashboardStats(
        totalPlants: 42,
        activePlants: 35,
        completedCycles: 7,
      );

      when(mockApiClient.get('/dashboard/stats'))
          .thenAnswer((_) async => mockStats.toJson());

      // Act
      final statsProvider = container.read(dashboardStatsProvider.future);
      final stats = await statsProvider;

      // Assert
      expect(stats.totalPlants, equals(42));
      expect(stats.activePlants, equals(35));
      verify(mockApiClient.get('/dashboard/stats')).called(1);
    });

    test('should handle loading state correctly', () async {
      // Arrange
      when(mockApiClient.get('/dashboard/stats'))
          .thenAnswer((_) async => Future.delayed(
                const Duration(seconds: 1),
                () => DashboardStats(
                  totalPlants: 0,
                  activePlants: 0,
                  completedCycles: 0,
                ).toJson(),
              ));

      // Act
      final asyncValue = container.read(dashboardStatsProvider);
      
      // Assert loading state
      expect(asyncValue.runtimeType, equals(AsyncLoading<DashboardStats>));

      // Wait for completion
      await container.read(dashboardStatsProvider.future);
      
      // Verify data state
      final completedValue = container.read(dashboardStatsProvider);
      expect(completedValue.runtimeType, equals(AsyncData<DashboardStats>));
      expect(completedValue.value?.totalPlants, equals(0));
    });

    test('should handle error state correctly', () async {
      // Arrange
      when(mockApiClient.get('/dashboard/stats'))
          .thenThrow(Exception('Network error'));

      // Act
      try {
        await container.read(dashboardStatsProvider.future);
        fail('Should have thrown an exception');
      } catch (e) {
        // Assert
        expect(e, isA<Exception>());
        verify(mockApiClient.get('/dashboard/stats')).called(1);
      }
    });
  });
}
```

## API Testing

### HTTP Client Testing
```dart
// test/unit/services/api_client_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:cultivar_app/core/api/api_client.dart';
import 'package:cultivar_app/core/api/api_exceptions.dart';

@GenerateMocks([http.Client])
import 'api_client_test.mocks.dart';

void main() {
  group('ApiClient Tests', () {
    late ApiClient apiClient;
    late MockHttpClient mockHttpClient;

    setUp(() {
      mockHttpClient = MockHttpClient();
      apiClient = ApiClient(
        baseUrl: 'https://api.cultivar.com',
        httpClient: mockHttpClient,
      );
    });

    test('should make GET request successfully', () async {
      // Arrange
      final responseBody = {'data': 'test'};
      final response = http.Response(jsonEncode(responseBody), 200);

      when(mockHttpClient.get(
        any,
        headers: anyNamed('headers'),
      )).thenAnswer((_) async => response);

      // Act
      final result = await apiClient.get('/test');

      // Assert
      expect(result, equals(responseBody));
      verify(mockHttpClient.get(
        'https://api.cultivar.com/test',
        headers: {'Content-Type': 'application/json'},
      )).called(1);
    });

    test('should throw ApiException for HTTP errors', () async {
      // Arrange
      final response = http.Response('Not Found', 404);
      
      when(mockHttpClient.get(any, headers: anyNamed('headers')))
          .thenAnswer((_) async => response);

      // Act & Assert
      expect(
        () => apiClient.get('/test'),
        throwsA(isA<ApiException>()),
      );
    });

    test('should handle timeout exceptions', () async {
      // Arrange
      when(mockHttpClient.get(any, headers: anyNamed('headers')))
          .thenThrow(TimeoutException('Request timeout'));

      // Act & Assert
      expect(
        () => apiClient.get('/test'),
        throwsA(isA<TimeoutException>()),
      );
    });
  });
}
```

## Error Handling and Edge Cases

### Comprehensive Error Testing
```dart
// test/unit/utils/validation_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/core/utils/validation.dart';

void main() {
  group('Validation Utils Tests', () {
    group('Email Validation', () {
      test('should validate correct email addresses', () {
        final validEmails = [
          'test@example.com',
          'user.name@domain.co.uk',
          'user+tag@example.org',
        ];

        for (final email in validEmails) {
          expect(ValidationUtils.isValidEmail(email), isTrue);
        }
      });

      test('should reject invalid email addresses', () {
        final invalidEmails = [
          'invalid-email',
          '@example.com',
          'user@',
          'user..double.dot@example.com',
          'user@example',
          '',
          null,
        ];

        for (final email in invalidEmails) {
          expect(ValidationUtils.isValidEmail(email), isFalse);
        }
      });
    });

    group('Plant Data Validation', () {
      test('should validate plant name requirements', () {
        expect(ValidationUtils.isValidPlantName('Valid Plant Name'), isTrue);
        expect(ValidationUtils.isValidPlantName('A'), isTrue); // Minimum 1 char
        expect(ValidationUtils.isValidPlantName(''), isFalse);
        expect(ValidationUtils.isValidPlantName('   '), isFalse);
        expect(ValidationUtils.isValidPlantName(null), isFalse);
      });

      test('should validate plant day range', () {
        expect(ValidationUtils.isValidPlantDay(0), isTrue); // Day 0 allowed
        expect(ValidationUtils.isValidPlantDay(1), isTrue);
        expect(ValidationUtils.isValidPlantDay(365), isTrue);
        expect(ValidationUtils.isValidPlantDay(-1), isFalse);
        expect(ValidationUtils.isValidPlantDay(366), isFalse);
      });
    });
  });
}
```

## Test Coverage Goals

### Coverage Requirements
- **Overall Coverage**: ≥80%
- **Business Logic**: ≥90%
- **UI Components**: ≥80%
- **API Integration**: ≥75%
- **Critical Paths**: 100%

### Coverage Commands
```bash
# Run tests with coverage
flutter test --coverage

# View coverage report
flutter pub run coverage:format_coverage --lcov --in=coverage/lcov.info --out=coverage.json

# Generate HTML report
genhtml coverage/lcov.info --output-directory=coverage/html

# Check specific file coverage
flutter test --coverage lib/features/plants/domain/plant_model.dart
```

### Coverage Exclusions
```yaml
# test/flutter_test_config.dart
import 'dart:io';

void main() {
  // Configure test environment
  HttpOverrides.global = null; // Allow real HTTP in tests if needed
  
  // Set test timeout
  setTestTimeout(const Timeout(Duration(minutes: 5)));
}

// .gitignore additions for coverage
coverage/
*.lcov
coverage.json
```

## Continuous Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/flutter_tests.yml
name: Flutter Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
        channel: 'stable'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Analyze code
      run: flutter analyze
    
    - name: Run tests
      run: flutter test --coverage
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
        flags: unittests
        name: codecov-umbrella
    
    - name: Check coverage threshold
      run: |
        COVERAGE=$(flutter pub run coverage:format_coverage --lcov --in=coverage/lcov.info --out=coverage.json | grep -o '"covered_lines": [0-9]*' | grep -o '[0-9]*')
        if [ "$COVERAGE" -lt 80 ]; then
          echo "Coverage $COVERAGE% is below 80% threshold"
          exit 1
        fi
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: coverage/
```

### Pre-commit Hooks
```bash
#!/bin/sh
# .git/hooks/pre-commit

echo "Running pre-commit tests..."

# Run tests
flutter test --reporter compact

# Check coverage
flutter test --coverage

# Analyze code
flutter analyze

# Format code
flutter format --set-exit-if-changed .

echo "Pre-commit checks passed!"
```

## Best Practices

### Test Organization
1. **AAA Pattern**: Arrange, Act, Assert
2. **Single Responsibility**: One test, one concept
3. **Descriptive Names**: Test names should explain what they test
4. **Setup/Teardown**: Use setUp and tearDown for common initialization
5. **Test Isolation**: Tests should not depend on each other

### Mock Usage Guidelines
1. **Mock External Dependencies**: APIs, databases, file system
2. **Don't Mock Value Objects**: Test real objects when possible
3. **Verify Interactions**: Ensure mocked methods are called correctly
4. **Use Stubs for Simple Cases**: When behavior is deterministic

### Performance Testing
```dart
// test/performance/login_performance_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/features/auth/screens/login_screen.dart';

void main() {
  group('Login Performance Tests', () {
    testWidgets('should login within 2 seconds', (WidgetTester tester) async {
      final stopwatch = Stopwatch()..start();

      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Simulate login process
      await tester.enterText(find.byKey(const Key('emailField')), 'test@example.com');
      await tester.enterText(find.byKey(const Key('passwordField')), 'password123');
      await tester.tap(find.byKey(const Key('loginButton')));
      await tester.pumpAndSettle();

      stopwatch.stop();

      // Assert performance
      expect(stopwatch.elapsedMilliseconds, lessThan(2000));
    });
  });
}
```

### Accessibility Testing
```dart
// test/accessibility/login_accessibility_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/features/auth/screens/login_screen.dart';
import 'package:flutter/material.dart';

void main() {
  group('Login Accessibility Tests', () {
    testWidgets('should have proper semantic labels', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Test form field accessibility
      expect(find.bySemanticsLabel('Email Address'), findsOneWidget);
      expect(find.bySemanticsLabel('Password'), findsOneWidget);
      
      // Test button accessibility
      expect(find.bySemanticsLabel('Sign In Button'), findsOneWidget);
    });

    testWidgets('should support keyboard navigation', (WidgetTester tester) async {
      await tester.pumpWidget(
        ProviderScope(
          child: MaterialApp(
            home: const LoginScreen(),
          ),
        ),
      );

      // Test tab navigation
      await tester.sendKeyEvent(LogicalKeyboardKey.tab);
      await tester.pump();
      
      // Should focus on email field
      expect(find.byKey(const Key('emailField')), findsOneWidget);
      
      await tester.sendKeyEvent(LogicalKeyboardKey.tab);
      await tester.pump();
      
      // Should focus on password field
      expect(find.byKey(const Key('passwordField')), findsOneWidget);
    });
  });
}
```

This comprehensive testing guide ensures CultivAR Flutter maintains high code quality, reliability, and user experience through systematic testing practices.
