import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:cultivar_app/features/auth/ui/login_screen.dart';

void main() {
  testWidgets('LoginScreen has a title and a login button', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(
      const ProviderScope(child: MaterialApp(home: LoginScreen())),
    );

    // Verify title
    expect(find.text('CultivAR'), findsOneWidget);

    // Verify login button
    expect(find.text('Login with CultivAR ID'), findsOneWidget);
  });
}
