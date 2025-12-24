import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:cultivar_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('End-to-end verification of Landing Page UI Polish', (
    WidgetTester tester,
  ) async {
    // 1. Launch the app
    app.main();
    await tester.pumpAndSettle();

    // 2. Verify "CultivAR" Logo Text Color (Navbar)
    final cultivarFinder = find.text('CultivAR');
    expect(cultivarFinder, findsAtLeastNWidgets(1));

    // We expect the one in the AppBar to be visible and have white color
    // NOTE: In integration tests, analyzing exact rendered pixels is hard,
    // but checking the widget style configuration is reliable.
    final navbarText = tester.widget<Text>(cultivarFinder.first);
    expect(
      navbarText.style?.color,
      Colors.white,
      reason: "Navbar 'CultivAR' text should be white",
    );

    // 3. Verify 'Become a Founder' Button Color
    final founderButtonFinder = find.widgetWithText(
      OutlinedButton,
      'Become a Founder',
    );
    expect(founderButtonFinder, findsOneWidget);

    final founderButton = tester.widget<OutlinedButton>(founderButtonFinder);
    // Resolve the foreground color state
    final Color? fgColor = founderButton.style?.foregroundColor?.resolve({});
    expect(
      fgColor,
      Colors.white,
      reason: "'Become a Founder' foreground should be white",
    );

    // 4. Verify "Read More" Buttons and Dialog Interaction
    final readMoreFinder = find.text('Read More');
    expect(readMoreFinder, findsAtLeastNWidgets(1));

    // Scroll to the first one (Environmental Control)
    await tester.scrollUntilVisible(readMoreFinder.first, 500);
    await tester.pumpAndSettle();

    // Tap it
    await tester.tap(readMoreFinder.first);
    await tester.pumpAndSettle();

    // Verify Dialog appears with mapped content
    expect(find.text('Environmental Control'), findsAtLeastNWidgets(1));
    expect(
      find.textContaining('optimize your climate'),
      findsNothing,
    ); // Old text if any
    expect(
      find.textContaining('Our system integrates with industry leaders'),
      findsOneWidget,
    ); // New generated text

    // Close Dialog
    await tester.tap(find.text('Close'));
    await tester.pumpAndSettle();

    // Verify closed
    expect(find.text('Close'), findsNothing);
  });
}
