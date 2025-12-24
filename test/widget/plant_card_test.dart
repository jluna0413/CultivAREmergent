// Disabled duplicate root-level test - moved to flutter_app/test/widgets/plant_card_test.dart
import 'package:cultivar_app/features/plants/domain/plant_model.dart';
import 'package:cultivar_app/features/plants/models/plant_metric.dart';
import 'package:cultivar_app/features/plants/widgets/plant_card.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:go_router/go_router.dart';
import 'package:mockito/mockito.dart';

// This test is intentionally disabled in the repo root - see flutter_app/test/widgets/plant_card_test.dart
// Mocks
class MockGoRouter extends Mock implements GoRouter {}

class MockBuildContext extends Mock implements BuildContext {}

void main() {
  // Disabled in this workspace. Use the Flutter package test under flutter_app instead.
  return;
  final mockPlant = Plant(
    id: 1,
    userId: 1,
    name: 'Test Plant',
    statusId: 2,
    statusName: 'Vegetative',
    description: 'Test Strain',
    startDt: DateTime.now().subtract(const Duration(days: 30)),
    imageUrl: 'https://example.com/image.jpg',
    // metrics property doesn't exist on domain Plant; tests should use PlantMetric models elsewhere
    // Placeholder fields may be ignored
      const PlantMetric(
        label: 'Height',
        value: '30',
        unit: 'cm',
        icon: Icons.height,
      ),
    ],
  );

  final mockPlantWithoutImage = mockPlant.copyWith(imageUrl: null);
  final mockPlantLongName = mockPlant.copyWith(
    name: 'This is a very long plant name that should overflow',
  );

  GoRouter mockGoRouter(WidgetTester tester) {
    final router = MockGoRouter();
    when(router.go(any)).thenAnswer((_) async {});
    return router;
  }

  Widget buildTestableWidget(Widget child, GoRouter router) {
    return MaterialApp(
      home: InheritedGoRouter(
        goRouter: router,
        child: Scaffold(body: child),
      ),
    );
  }

  group('PlantCard Widget Tests', () {
    testWidgets('Default card renders correctly', (WidgetTester tester) async {
      final router = mockGoRouter(tester);
      await tester.pumpWidget(
        buildTestableWidget(PlantCard(plant: mockPlant), router),
      );

      expect(find.text('Test Plant'), findsOneWidget);
      expect(find.text('Test Strain'), findsOneWidget);
      expect(find.byIcon(Icons.biotech), findsOneWidget);
      expect(find.text('30 days'), findsOneWidget);
      expect(find.text('A-1'), findsOneWidget);
      expect(find.text('30 cm'), findsOneWidget);
      expect(find.byType(Chip), findsOneWidget);
      expect(find.byIcon(Icons.visibility), findsOneWidget);
    });

    testWidgets('Compact card renders correctly', (WidgetTester tester) async {
      final router = mockGoRouter(tester);
      await tester.pumpWidget(
        buildTestableWidget(PlantCard(plant: mockPlant, compact: true), router),
      );

      expect(find.text('Test Plant'), findsOneWidget);
      expect(find.text('Test Strain'), findsOneWidget);
      expect(find.text('Age: 30 days'), findsOneWidget);
      // Metrics and full actions should not be visible
      expect(find.text('30 cm'), findsNothing);
      expect(find.byIcon(Icons.visibility), findsNothing);
      expect(
        find.byType(PopupMenuButton),
        findsNothing,
      ); // No edit/delete passed
    });

    testWidgets('Tapping default card navigates', (WidgetTester tester) async {
      final router = mockGoRouter(tester);
      var tapped = false;
      await tester.pumpWidget(
        buildTestableWidget(
          PlantCard(plant: mockPlant, onTap: () => tapped = true),
          router,
        ),
      );

      await tester.tap(find.byType(PlantCard));
      await tester.pump();

      expect(tapped, isTrue);
    });

    testWidgets('Tapping compact card navigates', (WidgetTester tester) async {
      final router = mockGoRouter(tester);
      var tapped = false;
      await tester.pumpWidget(
        buildTestableWidget(
          PlantCard(
            plant: mockPlant,
            compact: true,
            onTap: () => tapped = true,
          ),
          router,
        ),
      );

      await tester.tap(find.byType(PlantCard));
      await tester.pump();

      expect(tapped, isTrue);
    });

    testWidgets('Renders fallback icon when image URL is null', (
      WidgetTester tester,
    ) async {
      final router = mockGoRouter(tester);
      await tester.pumpWidget(
        buildTestableWidget(PlantCard(plant: mockPlantWithoutImage), router),
      );

      // CachedNetworkImage is not rendered, but the error/placeholder icon is.
      expect(find.byIcon(Icons.grass), findsOneWidget);
    });

    testWidgets('Long name ellipses in compact mode', (
      WidgetTester tester,
    ) async {
      final router = mockGoRouter(tester);
      await tester.pumpWidget(
        buildTestableWidget(
          SizedBox(
            width: 300,
            child: PlantCard(plant: mockPlantLongName, compact: true),
          ),
          router,
        ),
      );

      final text = tester.widget<Text>(
        find.text('This is a very long plant name that should overflow'),
      );
      expect(text.overflow, TextOverflow.ellipsis);
    });

    testWidgets('Action buttons are present and tappable', (
      WidgetTester tester,
    ) async {
      final router = mockGoRouter(tester);
      bool editTapped = false;
      bool deleteTapped = false;
      bool waterTapped = false;
      bool feedTapped = false;

      await tester.pumpWidget(
        buildTestableWidget(
          PlantCard(
            plant: mockPlant,
            onEdit: () => editTapped = true,
            onDelete: () => deleteTapped = true,
            onWater: () => waterTapped = true,
            onFeed: () => feedTapped = true,
          ),
          router,
        ),
      );

      await tester.tap(find.byIcon(Icons.edit));
      await tester.tap(find.byIcon(Icons.delete));
      await tester.tap(find.byIcon(Icons.water_drop));
      await tester.tap(find.byIcon(Icons.fastfood));
      await tester.pump();

      expect(editTapped, isTrue);
      expect(deleteTapped, isTrue);
      expect(waterTapped, isTrue);
      expect(feedTapped, isTrue);
    });

    testWidgets('Popup menu in compact mode works', (
      WidgetTester tester,
    ) async {
      final router = mockGoRouter(tester);
      bool editTapped = false;
      bool deleteTapped = false;

      await tester.pumpWidget(
        buildTestableWidget(
          PlantCard(
            plant: mockPlant,
            compact: true,
            onEdit: () => editTapped = true,
            onDelete: () => deleteTapped = true,
          ),
          router,
        ),
      );

      await tester.tap(find.byType(PopupMenuButton));
      await tester.pumpAndSettle(); // Wait for menu to appear

      await tester.tap(find.text('Edit'));
      await tester.pumpAndSettle();
      expect(editTapped, isTrue);

      await tester.tap(find.byType(PopupMenuButton));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Delete'));
      await tester.pumpAndSettle();
      expect(deleteTapped, isTrue);
    });
  });
}
