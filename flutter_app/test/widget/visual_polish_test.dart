import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/features/landing/ui/landing_screen.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  // Mock GoRouter to avoid actual navigation issues during test
  final GoRouter _router = GoRouter(
    routes: [
      GoRoute(path: '/', builder: (context, state) => const LandingScreen()),
      GoRoute(
        path: '/login',
        builder: (context, state) => const Scaffold(body: Text('Login Screen')),
      ),
      GoRoute(
        path: '/signup',
        builder: (context, state) =>
            const Scaffold(body: Text('Signup Screen')),
      ),
    ],
  );

  Widget createTestWidget() {
    return ProviderScope(
      child: MaterialApp.router(
        routerConfig: _router,
        theme: ThemeData(
          useMaterial3: true,
          colorScheme: ColorScheme.fromSeed(
            seedColor: const Color(0xFF00FF00),
            brightness: Brightness.dark,
          ),
        ),
      ),
    );
  }

  testWidgets('Landing Screen Visual Polish Verification', (
    WidgetTester tester,
  ) async {
    // 1. Pump the widget
    await tester.pumpWidget(createTestWidget());
    await tester.pumpAndSettle();

    // 2. Verify "CultivAR" Logo Text Color
    // Finding the Text widget with "CultivAR" (Nav bar or Hero)
    // Note: There are two "CultivAR" texts. One in AppBar/Nav, one in Hero.
    // We updated the Nav bar one to be explicitly white.

    final cultivarFinder = find.text('CultivAR');
    expect(cultivarFinder, findsAtLeastNWidgets(1));

    // Get the first Text widget (likely the navbar one since it's at the top)
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
    final buttonStyle = founderButton.style;

    // Check if the foreground color is white (MaterialStateProperty)
    // We set foregroundColor: Colors.white in the stlye
    expect(
      buttonStyle?.foregroundColor?.resolve({}),
      Colors.white,
      reason: "'Become a Founder' button foreground should be white",
    );

    // 4. Verify "Read More" Buttons and Dialogs
    // Find "Read More" buttons
    final readMoreFinder = find.text('Read More');
    expect(
      readMoreFinder,
      findsAtLeastNWidgets(1),
      reason: "Should find at least one 'Read More' button",
    );

    // Scroll to the first 'Read More' button to ensure it's visible (if in a list)
    await tester.scrollUntilVisible(readMoreFinder.first, 500);
    await tester.pumpAndSettle();

    // Tap the first "Read More" button (Environmental Control)
    await tester.tap(readMoreFinder.first);
    await tester.pumpAndSettle(); // Wait for dialog animation

    // 5. Verify Dialog Content
    // Expect the dialog title "Environmental Control"
    expect(
      find.text('Environmental Control'),
      findsAny,
    ); // Could find in list and dialog, so findsAny

    // Expect the detail content text
    expect(
      find.textContaining('Our system integrates with industry leaders'),
      findsOneWidget,
    );

    // Close the dialog
    await tester.tap(find.text('Close'));
    await tester.pumpAndSettle();

    // Dialog should be gone
    expect(find.text('Close'), findsNothing);
  });
}
