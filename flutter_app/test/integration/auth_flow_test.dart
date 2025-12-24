import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:cultivar_app/main.dart' as app;
import 'package:cultivar_app/features/auth/ui/login_screen.dart';
import 'package:cultivar_app/features/dashboard/ui/dashboard_screen.dart';
import 'package:cultivar_app/core/widgets/custom_text_field.dart';
import 'package:flutter/material.dart';

import 'package:flutter_secure_storage/flutter_secure_storage.dart';

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();
  FlutterSecureStorage.setMockInitialValues({});

  group('Auth Flow E2E', () {
    testWidgets('Full auth flow: login -> dashboard -> logout', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Verify initial login screen
      expect(find.byType(LoginScreen), findsOneWidget);

      // Enter credentials
      // Note: Adjust finders based on actual widget tree structure
      // Assuming CustomTextFields are present
      final emailField = find.widgetWithText(
        CustomTextField,
        'Email Address',
      ); // Adjust label if needed
      final passwordField = find.widgetWithText(
        CustomTextField,
        'Password',
      ); // Adjust label if needed

      // Fallback if CustomTextField is not found by text directly (it might be inside)
      // or if standard TextFormFields are used in LoginScreen (which seems to be the case in login_screen.dart)
      // login_screen.dart uses TextFormField directly, not CustomTextField.
      // So we should look for TextFormField.

      await tester.enterText(
        find.byType(TextFormField).at(0),
        'testuser@example.com',
      );
      await tester.enterText(find.byType(TextFormField).at(1), 'password');
      await tester.pump();

      // Tap login button
      await tester.tap(
        find.byType(ElevatedButton),
      ); // LoginScreen uses ElevatedButton
      await tester.pumpAndSettle();

      // Verify dashboard
      expect(find.byType(DashboardScreen), findsOneWidget);
      expect(find.text('CultivAR Dashboard'), findsOneWidget);

      // Tap logout
      await tester.tap(find.byIcon(Icons.logout));
      await tester.pumpAndSettle();

      // Back to login
      expect(find.byType(LoginScreen), findsOneWidget);
    });
  });
}
