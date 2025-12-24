# Flutter Testing Guide for CultivAR

## Testing Pyramid

- 70% Unit tests: Mock dependencies like ApiClient, test repository methods.
  Example:
  ```dart
  group('AuthRepository', () {
    test('login success', () async {
      when(mockApi.post(any)).thenAnswer((_) async => Response(data: tokenJson));
      final user = await repo.login('u', 'p');
      expect(user.username, 'u');
    });
    test('login failure throws AuthException', () async {
      when(mockApi.post(any)).thenThrow(AuthException('Invalid credentials'));
      expect(() => repo.login('bad', 'pass'), throwsA(isA<AuthException>()));
    });
  });
  ```

- 20% Widget tests: Test UI components in isolation.
  Example:
  ```dart
  testWidgets('Login form validates and shows error', (tester) async {
    await tester.pumpWidget(
      ProviderScope(
        overrides: [authNotifierProvider.overrideWith((ref) => mockNotifier)],
        child: MaterialApp(home: LoginScreen()),
      ),
    );
    expect(find.text('Welcome'), findsOneWidget);
    await tester.tap(find.byType(CustomButton));
    await tester.pump();
    expect(find.byType(LoadingIndicator), findsOneWidget);
    await tester.pump(const Duration(seconds: 1));
    expect(find.text('Invalid credentials'), findsOneWidget);
  });
  ```

- 10% Integration tests: E2E flows using integration_test package.
  Example:
  ```dart
  testWidgets('Auth flow', (tester) async {
    await tester.pumpWidget(ProviderScope(child: MyApp()));
    expect(find.byType(LoginScreen), findsOneWidget);
    await tester.enterText(find.byType(CustomTextField).first, 'user');
    await tester.enterText(find.byType(CustomTextField).at(1), 'pass');
    await tester.tap(find.byType(CustomButton));
    await tester.pumpAndSettle();
    expect(find.byType(DashboardScreen), findsOneWidget);
    // Tap logout button
    await tester.tap(find.text('Logout'));
    await tester.pumpAndSettle();
    expect(find.byType(LoginScreen), findsOneWidget);
  });
  ```

## Mocking

- Use mockito for API mocks.
- ProviderScope overrides for Riverpod providers in widget tests.
- test_backend for integration tests with mock API server.

## CI/CD

- `flutter test --coverage`
- Upload to codecov.io >80% coverage threshold.
- Fail CI if coverage <80%.

## Organization

- test/unit/ for repository/service unit tests
- test/widget/ for UI component tests
- test/integration/ for E2E flows