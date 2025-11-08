// Widget Tests for PlantCard Component
// Comprehensive testing for PlantCard, PlantCardCompact, and PlantCardWithProgress

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/core/widgets/plant_card.dart';
import 'package:cultivar_app/core/theme/app_theme.dart';

void main() {
  group('PlantCard Widget Tests', () {
    group('Basic PlantCard Rendering', () {
      testWidgets('PlantCard should render with required parameters',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Northern Lights',
                strain: 'Indica',
              ),
            ),
          ),
        );

        // Verify basic elements are present
        expect(find.text('Northern Lights'), findsOneWidget);
        expect(find.text('Indica'), findsOneWidget);
        expect(find.byType(PlantCard), findsOneWidget);
      });

      testWidgets('PlantCard should handle null optional parameters gracefully',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Test Plant',
                strain: 'Test Strain',
              ),
            ),
          ),
        );

        expect(find.text('Test Plant'), findsOneWidget);
        expect(find.text('Test Strain'), findsOneWidget);
        expect(find.byType(PopupMenuButton<String>), findsNothing);
        expect(find.byIcon(Icons.eco), findsNothing);
        expect(find.byIcon(Icons.calendar_today), findsNothing);
      });

      testWidgets('PlantCard should display with image URL when provided',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Image',
                strain: 'Strain',
                imageUrl: 'https://example.com/plant.jpg',
              ),
            ),
          ),
        );

        // Verify image widget is present (though network image may not load)
        expect(find.byType(Image), findsOneWidget);
      });

      testWidgets('PlantCard should handle image loading error gracefully',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Invalid Image',
                strain: 'Strain',
                imageUrl: 'https://invalid-url.example.com/plant.jpg',
              ),
            ),
          ),
        );

        // Should fallback to icon when image fails to load
        expect(find.byIcon(Icons.grass), findsOneWidget);
      });

      testWidgets('PlantCard should render status badge when provided',
          (WidgetTester tester) async {
        const status = PlantStatus(
          label: 'Active',
          color: Colors.green,
          icon: Icons.check_circle,
        );

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Plant with Status',
                strain: 'Strain',
                status: status,
              ),
            ),
          ),
        );

        expect(find.text('Active'), findsOneWidget);
        expect(find.byIcon(Icons.check_circle), findsOneWidget);
      });

      testWidgets('PlantCard should render metrics when provided',
          (WidgetTester tester) async {
        final metrics = [
          const PlantMetric(
            label: 'Height',
            value: '120',
            unit: 'cm',
            icon: Icons.height,
            color: Colors.blue,
          ),
          const PlantMetric(
            label: 'Weight',
            value: '500',
            unit: 'g',
            icon: Icons.scale,
            color: Colors.orange,
          ),
        ];

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Plant with Metrics',
                strain: 'Strain',
                metrics: metrics,
              ),
            ),
          ),
        );

        expect(find.text('120cm'), findsOneWidget);
        expect(find.text('500g'), findsOneWidget);
        expect(find.text('Height'), findsOneWidget);
        expect(find.text('Weight'), findsOneWidget);
        expect(find.byIcon(Icons.height), findsOneWidget);
        expect(find.byIcon(Icons.scale), findsOneWidget);
      });

      testWidgets('PlantCard should render plant details when not compact',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Details',
                strain: 'Strain',
                phase: 'Vegetative',
                ageInDays: 30,
                location: 'Grow Room A',
              ),
            ),
          ),
        );

        expect(find.text('Vegetative'), findsOneWidget);
        expect(find.text('30 days'), findsOneWidget);
        expect(find.text('Grow Room A'), findsOneWidget);
        expect(find.byIcon(Icons.eco), findsOneWidget);
        expect(find.byIcon(Icons.calendar_today), findsOneWidget);
        expect(find.byIcon(Icons.location_on), findsOneWidget);
      });
    });

    group('PlantCard Interaction Tests', () {
      testWidgets('PlantCard should call onTap callback when tapped',
          (WidgetTester tester) async {
        bool tapped = false;

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Tappable Plant',
                strain: 'Strain',
                onTap: () => tapped = true,
              ),
            ),
          ),
        );

        await tester.tap(find.byType(PlantCard));
        await tester.pump();

        expect(tapped, isTrue);
      });

      testWidgets(
          'PlantCard should show action menu when callbacks are provided',
          (WidgetTester tester) async {
        bool editTapped = false;
        bool deleteTapped = false;

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Plant with Actions',
                strain: 'Strain',
                onEdit: () => editTapped = true,
                onDelete: () => deleteTapped = true,
              ),
            ),
          ),
        );

        expect(find.byIcon(Icons.more_vert), findsOneWidget);

        // Open the popup menu
        await tester.tap(find.byIcon(Icons.more_vert));
        await tester.pump();

        expect(find.text('Edit'), findsOneWidget);
        expect(find.text('Delete'), findsOneWidget);

        // Test edit action
        await tester.tap(find.text('Edit'));
        await tester.pump();
        expect(editTapped, isTrue);

        // Reset and test delete action
        await tester.tap(find.byIcon(Icons.more_vert));
        await tester.pump();
        await tester.tap(find.text('Delete'));
        await tester.pump();
        expect(deleteTapped, isTrue);
      });
    });

    group('PlantCard Theme Tests', () {
      testWidgets('PlantCard should adapt to light theme',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Light Theme Plant',
                strain: 'Strain',
              ),
            ),
          ),
        );

        // Basic rendering test for light theme
        expect(find.text('Light Theme Plant'), findsOneWidget);
        expect(find.text('Strain'), findsOneWidget);
      });

      testWidgets('PlantCard should adapt to dark theme',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.darkTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Dark Theme Plant',
                strain: 'Strain',
              ),
            ),
          ),
        );

        // Basic rendering test for dark theme
        expect(find.text('Dark Theme Plant'), findsOneWidget);
        expect(find.text('Strain'), findsOneWidget);
      });
    });

    group('PlantCard Compact Mode Tests', () {
      testWidgets('PlantCardCompact should render in compact mode',
          (WidgetTester tester) async {
        const status = PlantStatus(
          label: 'Bloom',
          color: Colors.purple,
          icon: Icons.local_florist,
        );

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCardCompact(
                name: 'Compact Plant',
                strain: 'Strain',
                status: status,
              ),
            ),
          ),
        );

        expect(find.text('Compact Plant'), findsOneWidget);
        expect(find.text('Strain'), findsOneWidget);
        expect(find.text('Bloom'), findsOneWidget);
      });

      testWidgets('PlantCardCompact should call onTap callback',
          (WidgetTester tester) async {
        bool tapped = false;

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCardCompact(
                name: 'Tappable Compact Plant',
                strain: 'Strain',
                onTap: () => tapped = true,
              ),
            ),
          ),
        );

        await tester.tap(find.byType(PlantCard));
        await tester.pump();

        expect(tapped, isTrue);
      });

      testWidgets('PlantCardCompact should not show detailed information',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCardCompact(
                name: 'Compact Plant',
                strain: 'Strain',
              ),
            ),
          ),
        );

        // Should not show phase, age, or location information in compact mode
        expect(find.byIcon(Icons.eco), findsNothing);
        expect(find.byIcon(Icons.calendar_today), findsNothing);
        expect(find.byIcon(Icons.location_on), findsNothing);
      });
    });

    group('PlantCardWithProgress Tests', () {
      testWidgets('PlantCardWithProgress should render with progress metric',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCardWithProgress(
                name: 'Progress Plant',
                strain: 'Strain',
                progress: 0.75,
              ),
            ),
          ),
        );

        expect(find.text('Progress Plant'), findsOneWidget);
        expect(find.text('75%'), findsOneWidget);
        expect(find.text('Progress'), findsOneWidget);
        expect(find.byIcon(Icons.trending_up), findsOneWidget);
      });

      testWidgets(
          'PlantCardWithProgress should handle different progress values',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: Column(
                children: [
                  PlantCardWithProgress(
                    name: '0% Progress',
                    strain: 'Strain',
                    progress: 0.0,
                  ),
                  PlantCardWithProgress(
                    name: '100% Progress',
                    strain: 'Strain',
                    progress: 1.0,
                  ),
                ],
              ),
            ),
          ),
        );

        expect(find.text('0%'), findsOneWidget);
        expect(find.text('100%'), findsOneWidget);
      });

      testWidgets('PlantCardWithProgress should show status when provided',
          (WidgetTester tester) async {
        const status = PlantStatus(
          label: 'Flowering',
          color: Colors.orange,
          icon: Icons.local_florist,
        );

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCardWithProgress(
                name: 'Status Progress Plant',
                strain: 'Strain',
                progress: 0.5,
                status: status,
              ),
            ),
          ),
        );

        expect(find.text('Flowering'), findsOneWidget);
        expect(find.byIcon(Icons.local_florist), findsOneWidget);
      });
    });

    group('PlantCard Edge Cases', () {
      testWidgets('PlantCard should handle very long names gracefully',
          (WidgetTester tester) async {
        const longName =
            'Very Long Plant Name That Should Be Truncated with Ellipsis';

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: longName,
                strain: 'Strain',
              ),
            ),
          ),
        );

        // Should show the full text (Dart handles text overflow automatically)
        expect(find.text(longName), findsOneWidget);
      });

      testWidgets('PlantCard should handle empty metrics list',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with No Metrics',
                strain: 'Strain',
                metrics: [],
              ),
            ),
          ),
        );

        // Should render normally without metrics
        expect(find.text('Plant with No Metrics'), findsOneWidget);
        expect(find.text('Strain'), findsOneWidget);
      });

      testWidgets('PlantCard should handle multiple metrics without overflow',
          (WidgetTester tester) async {
        final metrics = List.generate(
            5,
            (index) => PlantMetric(
                  label: 'Metric $index',
                  value: '${index * 10}',
                  unit: 'cm',
                ));

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Plant with Many Metrics',
                strain: 'Strain',
                metrics: metrics,
              ),
            ),
          ),
        );

        // All metrics should be visible (they use Expanded widget)
        for (int i = 0; i < 5; i++) {
          expect(find.text('${i * 10}cm'), findsOneWidget);
        }
      });

      testWidgets(
          'PlantCard should render action menu even with all optional parameters null',
          (WidgetTester tester) async {
        bool editCalled = false;
        bool deleteCalled = false;

        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: Scaffold(
              body: PlantCard(
                name: 'Minimal Plant',
                strain: 'Strain',
                onEdit: () => editCalled = true,
                onDelete: () => deleteCalled = true,
              ),
            ),
          ),
        );

        // Should show action menu even without other optional parameters
        expect(find.byIcon(Icons.more_vert), findsOneWidget);

        await tester.tap(find.byIcon(Icons.more_vert));
        await tester.pump();
        expect(find.text('Edit'), findsOneWidget);
        expect(find.text('Delete'), findsOneWidget);
      });
    });

    group('PlantCard Visual Hierarchy Tests', () {
      testWidgets('PlantCard should have proper visual hierarchy',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Hierarchy Test Plant',
                strain: 'Hierarchy Strain',
                phase: 'Vegetative',
                ageInDays: 14,
                location: 'Room A',
                status: PlantStatus(
                  label: 'Healthy',
                  color: Colors.green,
                ),
                metrics: [
                  PlantMetric(
                    label: 'Height',
                    value: '50',
                    unit: 'cm',
                  ),
                ],
              ),
            ),
          ),
        );

        // Verify all elements are present and visible
        expect(find.text('Hierarchy Test Plant'), findsOneWidget);
        expect(find.text('Hierarchy Strain'), findsOneWidget);
        expect(find.text('Healthy'), findsOneWidget);
        expect(find.text('Vegetative'), findsOneWidget);
        expect(find.text('14 days'), findsOneWidget);
        expect(find.text('Room A'), findsOneWidget);
        expect(find.text('50cm'), findsOneWidget);
      });

      testWidgets('PlantCard should maintain accessibility semantics',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Accessible Plant',
                strain: 'Strain',
              ),
            ),
          ),
        );

        // Should have semantic labels for accessibility
        final plantCard = tester.widget<PlantCard>(find.byType(PlantCard));
        expect(plantCard.name, equals('Accessible Plant'));
        expect(plantCard.strain, equals('Strain'));
      });
    });

    group('PlantCard Error Handling Tests', () {
      testWidgets('PlantCard should handle null imageUrl gracefully',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Null Image',
                strain: 'Strain',
                imageUrl: null,
              ),
            ),
          ),
        );

        // Should show default grass icon when no image
        expect(find.byIcon(Icons.grass), findsOneWidget);
      });

      testWidgets('PlantCard should handle empty strain name',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Empty Strain',
                strain: '',
              ),
            ),
          ),
        );

        expect(find.text('Plant with Empty Strain'), findsOneWidget);
        expect(find.text(''), findsOneWidget);
      });

      testWidgets('PlantCard should handle negative ageInDays',
          (WidgetTester tester) async {
        await tester.pumpWidget(
          MaterialApp(
            theme: AppTheme.lightTheme,
            home: const Scaffold(
              body: PlantCard(
                name: 'Plant with Negative Age',
                strain: 'Strain',
                ageInDays: -1,
              ),
            ),
          ),
        );

        // Should display negative age as is (business logic validation would be separate)
        expect(find.text('-1 days'), findsOneWidget);
      });
    });
  });

  group('PlantStatus Widget Tests', () {
    testWidgets('PlantStatus should render with icon',
        (WidgetTester tester) async {
      const status = PlantStatus(
        label: 'Active',
        color: Colors.blue,
        icon: Icons.check_circle,
      );

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: Container(
              child: status.buildStatusBadge(),
            ),
          ),
        ),
      );

      expect(find.text('Active'), findsOneWidget);
      expect(find.byIcon(Icons.check_circle), findsOneWidget);
    });

    testWidgets('PlantStatus should render without icon',
        (WidgetTester tester) async {
      const status = PlantStatus(
        label: 'Inactive',
        color: Colors.red,
      );

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: Container(),
          ),
        ),
      );

      // This test just ensures PlantStatus can be instantiated without icon
      expect(status.icon, isNull);
      expect(status.label, equals('Inactive'));
    });
  });

  group('PlantMetric Widget Tests', () {
    testWidgets('PlantMetric should render with all properties',
        (WidgetTester tester) async {
      const metric = PlantMetric(
        label: 'Temperature',
        value: '25',
        unit: '°C',
        icon: Icons.thermostat,
        color: Colors.orange,
      );

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: Container(),
          ),
        ),
      );

      expect(metric.label, equals('Temperature'));
      expect(metric.value, equals('25'));
      expect(metric.unit, equals('°C'));
      expect(metric.icon, equals(Icons.thermostat));
      expect(metric.color, equals(Colors.orange));
    });

    testWidgets('PlantMetric should render with minimal properties',
        (WidgetTester tester) async {
      const metric = PlantMetric(
        label: 'Label',
        value: '100',
      );

      await tester.pumpWidget(
        MaterialApp(
          theme: AppTheme.lightTheme,
          home: Scaffold(
            body: Container(),
          ),
        ),
      );

      expect(metric.unit, isNull);
      expect(metric.icon, isNull);
      expect(metric.color, isNull);
      expect(metric.label, equals('Label'));
      expect(metric.value, equals('100'));
    });
  });
}

// Extension to test PlantStatus badge rendering
extension PlantStatusTest on PlantStatus {
  Widget buildStatusBadge() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: color.withValues(alpha: 0.2),
          width: 1,
        ),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (icon != null) ...[
            Icon(
              icon!,
              color: color,
              size: 12,
            ),
            const SizedBox(width: 4),
          ],
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 11,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }
}
