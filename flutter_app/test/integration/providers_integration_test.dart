// Integration Tests for Providers
// Tests provider-to-provider dependencies and data flow

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cultivar_app/core/providers/plants_provider.dart';
import 'package:cultivar_app/core/providers/auth_provider.dart';
import 'package:cultivar_app/core/providers/cultivar_provider.dart';
import 'package:cultivar_app/core/models/plant_models.dart';
import 'package:cultivar_app/core/models/cultivar_models.dart';

void main() {
  group('Provider Integration Tests', () {
    late ProviderContainer container;

    setUp(() {
      container = ProviderContainer();
    });

    tearDown(() {
      container.dispose();
    });

    group('PlantsProvider Integration', () {
      testWidgets('PlantsProvider should initialize with empty state', (WidgetTester tester) async {
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        final plantsProvider = container.read(plantsProvider);
        expect(plantsProvider, equals(isA<AsyncValue<List<Plant>>>()));
      });

      testWidgets('PlantsProvider should handle loading state', (WidgetTester tester) async {
        // Mock loading state
        container.read(plantsProvider.notifier).setState(const AsyncValue.loading());

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        expect(find.text('Loading...'), findsOneWidget);
      });

      testWidgets('PlantsProvider should handle error state', (WidgetTester tester) async {
        // Mock error state
        container.read(plantsProvider.notifier).setState(
          const AsyncValue.error('Test error', StackTrace.empty),
        );

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        expect(find.text('Test error'), findsOneWidget);
      });

      testWidgets('PlantsProvider should display plants when loaded', (WidgetTester tester) async {
        // Mock loaded state with test data
        final testPlants = [
          Plant(
            id: 1,
            name: 'Test Plant 1',
            description: 'Description 1',
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
          ),
          Plant(
            id: 2,
            name: 'Test Plant 2',
            description: 'Description 2',
            statusId: 1,
            cultivarId: 2,
            isClone: true,
            autoflower: true,
            startDate: DateTime(2024, 2, 1),
            lastWaterDate: DateTime(2024, 2, 15),
            lastFeedDate: DateTime(2024, 2, 10),
            harvestDate: DateTime(2024, 5, 1),
            userId: 1,
            createdAt: DateTime(2024, 2, 1),
            updatedAt: DateTime(2024, 2, 1),
          ),
        ];

        container.read(plantsProvider.notifier).setState(AsyncValue.data(testPlants));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        expect(find.text('Test Plant 1'), findsOneWidget);
        expect(find.text('Test Plant 2'), findsOneWidget);
      });
    });

    group('AuthProvider Integration', () {
      testWidgets('AuthProvider should manage authentication state', (WidgetTester tester) async {
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: AuthStatusWidget(),
              ),
            ),
          ),
        );

        final authProvider = container.read(authProvider);
        expect(authProvider, equals(isA<AsyncValue<User>>()));
      });

      testWidgets('AuthProvider should handle login flow', (WidgetTester tester) async {
        // Mock successful login
        final mockUser = User(
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          isAdmin: false,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        container.read(authProvider.notifier).setState(AsyncValue.data(mockUser));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: AuthStatusWidget(),
              ),
            ),
          ),
        );

        expect(find.text('testuser'), findsOneWidget);
        expect(find.text('Login'), findsNothing);
        expect(find.text('Logout'), findsOneWidget);
      });

      testWidgets('AuthProvider should handle logout', (WidgetTester tester) async {
        // Start with logged in state
        final mockUser = User(
          id: 1,
          username: 'testuser',
          email: 'test@example.com',
          isAdmin: false,
          createdAt: DateTime.now(),
          updatedAt: DateTime.now(),
        );

        container.read(authProvider.notifier).setState(AsyncValue.data(mockUser));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: AuthStatusWidget(),
              ),
            ),
          ),
        );

        // Verify logout
        container.read(authProvider.notifier).setState(const AsyncValue.loading());

        await tester.pump();
        expect(find.text('Login'), findsOneWidget);
        expect(find.text('Logout'), findsNothing);
      });
    });

    group('CultivarProvider Integration', () {
      testWidgets('CultivarProvider should integrate with PlantsProvider', (WidgetTester tester) async {
        final testCultivars = [
          Cultivar(
            id: 1,
            name: 'Northern Lights',
            type: 'Indica',
            description: 'Classic indica strain',
            thc: 18.5,
            cbd: 2.1,
            floweringTime: 8,
            yield: '500-600g/m²',
            createdAt: DateTime(2024, 1, 1),
            updatedAt: DateTime(2024, 1, 1),
          ),
          Cultivar(
            id: 2,
            name: 'Super Lemon Haze',
            type: 'Sativa',
            description: 'Energizing sativa strain',
            thc: 22.0,
            cbd: 1.5,
            floweringTime: 10,
            yield: '600-700g/m²',
            createdAt: DateTime(2024, 1, 1),
            updatedAt: DateTime(2024, 1, 1),
          ),
        ];

        container.read(cultivarsProvider.notifier).setState(AsyncValue.data(testCultivars));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: CultivarsListWidget(),
              ),
            ),
          ),
        );

        expect(find.text('Northern Lights'), findsOneWidget);
        expect(find.text('Super Lemon Haze'), findsOneWidget);
        expect(find.text('Indica'), findsOneWidget);
        expect(find.text('Sativa'), findsOneWidget);
      });
    });

    group('Cross-Provider Integration', () {
      testWidgets('Plants and Cultivars should integrate properly', (WidgetTester tester) async {
        // Set up cultivars first
        final testCultivars = [
          Cultivar(
            id: 1,
            name: 'Northern Lights',
            type: 'Indica',
            description: 'Classic indica strain',
            thc: 18.5,
            cbd: 2.1,
            floweringTime: 8,
            yield: '500-600g/m²',
            createdAt: DateTime(2024, 1, 1),
            updatedAt: DateTime(2024, 1, 1),
          ),
        ];

        container.read(cultivarsProvider.notifier).setState(AsyncValue.data(testCultivars));

        // Set up plants with cultivar relationships
        final testPlants = [
          Plant(
            id: 1,
            name: 'My Northern Lights',
            description: 'My first plant',
            statusId: 1,
            cultivarId: 1, // Reference to cultivar above
            isClone: false,
            autoflower: false,
            startDate: DateTime(2024, 1, 1),
            lastWaterDate: DateTime(2024, 1, 15),
            lastFeedDate: DateTime(2024, 1, 10),
            harvestDate: DateTime(2024, 4, 1),
            userId: 1,
            createdAt: DateTime(2024, 1, 1),
            updatedAt: DateTime(2024, 1, 1),
          ),
        ];

        container.read(plantsProvider.notifier).setState(AsyncValue.data(testPlants));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsWithCultivarsWidget(),
              ),
            ),
          ),
        );

        // Verify plant shows cultivar information
        expect(find.text('My Northern Lights'), findsOneWidget);
        expect(find.text('Northern Lights'), findsOneWidget);
      });
    });

    group('Provider Error Handling Integration', () {
      testWidgets('Providers should handle network errors gracefully', (WidgetTester tester) async {
        // Simulate network error in plants provider
        container.read(plantsProvider.notifier).setState(
          const AsyncValue.error('Network error', StackTrace.empty),
        );

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: ErrorHandlingWidget(),
              ),
            ),
          ),
        );

        expect(find.text('Network error'), findsOneWidget);
        expect(find.text('Retry'), findsOneWidget);
      });

      testWidgets('Providers should handle loading states across components', (WidgetTester tester) async {
        // Simulate loading in multiple providers
        container.read(plantsProvider.notifier).setState(const AsyncValue.loading());
        container.read(cultivarsProvider.notifier).setState(const AsyncValue.loading());
        container.read(authProvider.notifier).setState(const AsyncValue.loading());

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: LoadingStatesWidget(),
              ),
            ),
          ),
        );

        // Should show loading indicators
        expect(find.byType(CircularProgressIndicator), findsWidgets);
      });
    });

    group('Provider State Persistence Integration', () {
      testWidgets('Provider state should persist across widget rebuilds', (WidgetTester tester) async {
        final testPlants = [
          Plant(
            id: 1,
            name: 'Persistent Plant',
            description: 'Should persist',
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
          ),
        ];

        container.read(plantsProvider.notifier).setState(AsyncValue.data(testPlants));

        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        // First build - should show plant
        expect(find.text('Persistent Plant'), findsOneWidget);

        // Force rebuild
        await tester.pumpWidget(
          UncontrolledProviderScope(
            container: container,
            child: const MaterialApp(
              home: Scaffold(
                body: PlantsListWidget(),
              ),
            ),
          ),
        );

        // State should persist - plant should still be visible
        expect(find.text('Persistent Plant'), findsOneWidget);
      });
    });
  });
}

// Mock widgets for testing
class PlantsListWidget extends ConsumerWidget {
  const PlantsListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plants = ref.watch(plantsProvider);
    
    return plants.when(
      data: (plantList) => Column(
        children: plantList.map((plant) => Text(plant.name)).toList(),
      ),
      loading: () => const Text('Loading...'),
      error: (error, stack) => Text(error.toString()),
    );
  }
}

class AuthStatusWidget extends ConsumerWidget {
  const AuthStatusWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final auth = ref.watch(authProvider);
    
    return auth.when(
      data: (user) => Column(
        children: [
          Text(user.username),
          ElevatedButton(
            onPressed: () {
              ref.read(authProvider.notifier).setState(const AsyncValue.loading());
            },
            child: const Text('Logout'),
          ),
        ],
      ),
      loading: () => const Text('Login'),
      error: (error, stack) => const Text('Login'),
    );
  }
}

class CultivarsListWidget extends ConsumerWidget {
  const CultivarsListWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final cultivars = ref.watch(cultivarsProvider);
    
    return cultivars.when(
      data: (cultivarList) => Column(
        children: cultivarList.map((cultivar) => Column(
          children: [
            Text(cultivar.name),
            Text(cultivar.type),
          ],
        )).toList(),
      ),
      loading: () => const Text('Loading cultivars...'),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}

class PlantsWithCultivarsWidget extends ConsumerWidget {
  const PlantsWithCultivarsWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plants = ref.watch(plantsProvider);
    final cultivars = ref.watch(cultivarsProvider);
    
    return plants.when(
      data: (plantList) => cultivars.when(
        data: (cultivarList) => Column(
          children: plantList.map((plant) {
            final cultivar = cultivarList.firstWhere(
              (c) => c.id == plant.cultivarId,
              orElse: () => Cultivar(
                id: 0,
                name: 'Unknown',
                type: 'Unknown',
                description: '',
                thc: 0,
                cbd: 0,
                floweringTime: 0,
                yield: '',
                createdAt: DateTime.now(),
                updatedAt: DateTime.now(),
              ),
            );
            return Column(
              children: [
                Text(plant.name),
                Text(cultivar.name),
              ],
            );
          }).toList(),
        ),
        loading: () => const Text('Loading cultivars...'),
        error: (error, stack) => Text('Cultivar Error: $error'),
      ),
      loading: () => const Text('Loading plants...'),
      error: (error, stack) => Text('Plant Error: $error'),
    );
  }
}

class ErrorHandlingWidget extends ConsumerWidget {
  const ErrorHandlingWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plants = ref.watch(plantsProvider);
    
    return plants.when(
      data: (plantList) => const Text('No plants'),
      loading: () => const Text('Loading...'),
      error: (error, stack) => Column(
        children: [
          Text('Error: $error'),
          ElevatedButton(
            onPressed: () {
              // Retry action would go here
            },
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }
}

class LoadingStatesWidget extends ConsumerWidget {
  const LoadingStatesWidget({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plants = ref.watch(plantsProvider);
    final cultivars = ref.watch(cultivarsProvider);
    final auth = ref.watch(authProvider);
    
    return Column(
      children: [
        plants.when(
          data: (plantList) => const Text('Plants loaded'),
          loading: () => const CircularProgressIndicator(),
          error: (error, stack) => const Text('Plants error'),
        ),
        cultivars.when(
          data: (cultivarList) => const Text('Cultivars loaded'),
          loading: () => const CircularProgressIndicator(),
          error: (error, stack) => const Text('Cultivars error'),
        ),
        auth.when(
          data: (user) => const Text('Authenticated'),
          loading: () => const CircularProgressIndicator(),
          error: (error, stack) => const Text('Auth error'),
        ),
      ],
    );
  }
}