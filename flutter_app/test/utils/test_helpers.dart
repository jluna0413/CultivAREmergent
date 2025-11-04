// Test Helpers for CultivAREmergant Flutter App
// Comprehensive testing utilities for unit, widget, integration, and E2E tests

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:cultivar_app/core/models/plant_models.dart';
import 'package:cultivar_app/models/cultivar.dart' as cultivar_models;
import 'package:cultivar_app/core/models/sensor_models.dart';
import 'package:cultivar_app/core/models/user_models.dart' as user_models;
import 'package:cultivar_app/core/models/cart_models.dart';
import 'package:cultivar_app/core/models/dashboard_stats.dart';
import 'package:cultivar_app/core/models/auth_models.dart' as auth_models;

// Mock API Client for testing
class MockApiClient {
  static final List<Plant> _plants = [];
  static final List<cultivar_models.Cultivar> _cultivars = [];
  static final List<Sensor> _sensors = [];
  static final List<user_models.User> _users = [];
  static final List<CartItem> _cartItems = [];
  static auth_models.User? _currentUser;

  static Future<List<Plant>> getPlants() async => _plants;
  static Future<List<cultivar_models.Cultivar>> getCultivars() async =>
      _cultivars;
  static Future<List<Sensor>> getSensors() async => _sensors;
  static Future<List<user_models.User>> getUsers() async => _users;
  static Future<List<CartItem>> getCartItems() async => _cartItems;
  static Future<auth_models.User?> getCurrentUser() async => _currentUser;
  static Future<bool> login(String email, String password) async {
    _currentUser = TestDataFactory.createTestAuthUser(email: email);
    return true;
  }

  static Future<void> logout() async => _currentUser = null;

  static void addPlant(Plant plant) => _plants.add(plant);
  static void addCultivar(cultivar_models.Cultivar cultivar) =>
      _cultivars.add(cultivar);
  static void addSensor(Sensor sensor) => _sensors.add(sensor);
  static void addUser(user_models.User user) => _users.add(user);
  static void addCartItem(CartItem item) => _cartItems.add(item);
  static void clearAll() {
    _plants.clear();
    _cultivars.clear();
    _sensors.clear();
    _users.clear();
    _cartItems.clear();
    _currentUser = null;
  }
}

// Test Data Factory
class TestDataFactory {
  // Plant Test Data Factory
  static Plant createTestPlant({
    int? id,
    String? name,
    String? description,
    int? statusId,
    int? cultivarId,
    bool? isClone,
    bool? autoflower,
    DateTime? startDate,
    DateTime? lastWaterDate,
    DateTime? lastFeedDate,
    DateTime? harvestDate,
    int? userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    final now = DateTime.now();
    return Plant(
      id: id ?? 1,
      name: name ?? 'Test Plant',
      description: description ?? 'Test plant description',
      statusId: statusId ?? 1,
      cultivarId: cultivarId,
      isClone: isClone ?? false,
      autoflower: autoflower ?? false,
      startDate: startDate ?? now,
      lastWaterDate: lastWaterDate ?? now,
      lastFeedDate: lastFeedDate ?? now,
      harvestDate: harvestDate,
      userId: userId ?? 1,
      createdAt: createdAt ?? now,
      updatedAt: updatedAt ?? now,
    );
  }

  // Cultivar Test Data Factory (using the correct Cultivar model)
  static cultivar_models.Cultivar createTestCultivar({
    int? id,
    int? userId,
    String? name,
    int? indica,
    int? sativa,
    bool? autoflower,
    String? description,
    String? shortDescription,
    int? seedCount,
  }) {
    return cultivar_models.Cultivar(
      id: id ?? 1,
      userId: userId ?? 1,
      name: name ?? 'Northern Lights',
      indica: indica ?? 80,
      sativa: sativa ?? 20,
      autoflower: autoflower ?? false,
      seedCount: seedCount ?? 10,
      description: description,
      shortDescription: shortDescription,
    );
  }

  // Sensor Test Data Factory
  static Sensor createTestSensor({
    int? id,
    String? name,
    String? description,
    String? type,
    String? model,
    String? location,
    String? zone,
    SensorStatus? status,
    String? apiEndpoint,
    String? apiKey,
    String? unit,
    double? minThreshold,
    double? maxThreshold,
    bool? isActive,
    DateTime? lastReading,
    double? value,
    SensorHealth? health,
    String? firmware,
  }) {
    final now = DateTime.now();
    return Sensor(
      id: id ?? 1,
      name: name ?? 'Test Sensor',
      description: description ?? 'Test sensor description',
      type: type ?? 'temperature',
      model: model ?? 'DHT22',
      location: location ?? 'Grow Room 1',
      zone: zone ?? 'Zone A',
      status: status ?? SensorStatus.online,
      apiEndpoint: apiEndpoint ?? 'https://api.example.com',
      apiKey: apiKey ?? 'test_api_key',
      unit: unit ?? '°C',
      minThreshold: minThreshold ?? 0.0,
      maxThreshold: maxThreshold ?? 50.0,
      isActive: isActive ?? true,
      lastReading: lastReading ?? now,
      value: value ?? 25.0,
      health: health ?? SensorHealth.good,
      firmware: firmware ?? '1.0.0',
      createdAt: now,
      updatedAt: now,
    );
  }

  // User Test Data Factory (using user_models.User)
  static user_models.User createTestUser({
    int? id,
    String? username,
    String? email,
    bool? isActive,
    String? firstName,
    String? lastName,
    user_models.UserRole? role,
    user_models.UserStatus? status,
  }) {
    final now = DateTime.now();
    return user_models.User(
      id: id ?? 1,
      username: username ?? 'testuser',
      email: email ?? 'test@example.com',
      isActive: isActive ?? true,
      createdAt: now,
      firstName: firstName ?? 'Test',
      lastName: lastName ?? 'User',
      role: role ?? user_models.UserRole.user,
      status: status ?? user_models.UserStatus.active,
    );
  }

  // Auth User Test Data Factory (using auth_models.User)
  static auth_models.User createTestAuthUser({
    int? id,
    String? email,
    String? username,
    String? avatar,
    bool? isActive,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    final now = DateTime.now();
    return auth_models.User(
      id: id ?? 1,
      email: email ?? 'test@example.com',
      username: username ?? 'testuser',
      avatar: avatar,
      createdAt: createdAt ?? now,
      updatedAt: updatedAt ?? now,
      isActive: isActive ?? true,
    );
  }

  // Cart Item Test Data Factory
  static CartItem createTestCartItem({
    int? id,
    int? productId,
    String? productName,
    double? price,
    int? quantity,
    String? imageUrl,
    String? description,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    final now = DateTime.now();
    return CartItem(
      id: id ?? 1,
      productId: productId ?? 1,
      productName: productName ?? 'Northern Lights Seeds',
      price: price ?? 15.99,
      quantity: quantity ?? 1,
      imageUrl: imageUrl,
      description: description,
      productData: null,
      createdAt: createdAt ?? now,
      updatedAt: updatedAt ?? now,
    );
  }

  // Dashboard Stats Test Data Factory
  static DashboardStats createTestDashboardStats({
    CountStats? counts,
    CultivarStats? cultivars,
    EnvironmentalStats? environment,
    SensorStats? sensors,
    EnvironmentalSlice? dataSlices,
    DateTime? generatedAt,
    int? userId,
  }) {
    return DashboardStats(
      counts: counts ??
          CountStats(
              total: 10,
              active: 8,
              harvested: 2,
              seedlings: 3,
              vegetative: 3,
              flowering: 2),
      cultivars:
          cultivars ?? CultivarStats(totalCultivars: 5, userCultivars: 3),
      environment: environment ??
          EnvironmentalStats(
              avgTemperature: 24.5, avgHumidity: 65.0, avgPh: 6.2),
      sensors: sensors ?? SensorStats(totalSensors: 5, activeSensors: 4),
      dataSlices: dataSlices ?? EnvironmentalSlice(),
      growthPhases: [],
      recentReadings: [],
      recentActivities: [],
      generatedAt: generatedAt ?? DateTime.now(),
      userId: userId ?? 1,
    );
  }

  // Auth Response Test Data Factory
  static auth_models.AuthResponse createTestAuthResponse({
    auth_models.User? user,
    String? accessToken,
    String? tokenType,
    String? refreshToken,
  }) {
    return auth_models.AuthResponse(
      accessToken: accessToken ?? 'test_token_123',
      tokenType: tokenType ?? 'Bearer',
      user: user ?? createTestAuthUser(),
      refreshToken: refreshToken,
    );
  }
}

// Test Matchers for CultivAREmergant
class CultivaremantTestMatchers {
  static Matcher isValidPlant() {
    return predicate<Plant>(
        (plant) =>
            plant.id != null && plant.name.isNotEmpty && plant.userId != null,
        'is a valid Plant');
  }

  static Matcher isValidCultivar() {
    return predicate<cultivar_models.Cultivar>(
        (cultivar) =>
            cultivar.id != null &&
            cultivar.name.isNotEmpty &&
            cultivar.userId != null &&
            (cultivar.indica ?? 0) >= 0 &&
            (cultivar.sativa ?? 0) >= 0,
        'is a valid Cultivar');
  }

  static Matcher isValidSensor() {
    return predicate<Sensor>(
        (sensor) =>
            sensor.id != null &&
            sensor.name.isNotEmpty &&
            sensor.type.isNotEmpty,
        'is a valid Sensor');
  }

  static Matcher isValidUser() {
    return predicate<user_models.User>(
        (user) =>
            user.id != null &&
            user.username.isNotEmpty &&
            user.email.isNotEmpty,
        'is a valid User');
  }

  static Matcher isValidAuthUser() {
    return predicate<auth_models.User>(
        (user) =>
            user.id > 0 && user.username.isNotEmpty && user.email.isNotEmpty,
        'is a valid Auth User');
  }

  static Matcher hasValidPlantData() {
    return predicate<Plant>(
        (plant) => plant.id > 0 && plant.name.isNotEmpty && plant.statusId > 0,
        'has valid plant data');
  }

  static Matcher hasValidSensorData() {
    return predicate<Sensor>(
        (sensor) =>
            sensor.id > 0 && sensor.name.isNotEmpty && sensor.type.isNotEmpty,
        'has valid sensor data');
  }

  static Matcher hasValidUserData() {
    return predicate<user_models.User>(
        (user) =>
            user.id > 0 && user.username.isNotEmpty && user.email.isNotEmpty,
        'has valid user data');
  }

  static Matcher hasValidCultivarData() {
    return predicate<cultivar_models.Cultivar>(
        (cultivar) =>
            (cultivar.id ?? 0) > 0 &&
            cultivar.name.isNotEmpty &&
            (cultivar.indica ?? 0) >= 0 &&
            (cultivar.sativa ?? 0) >= 0,
        'has valid cultivar data');
  }
}

// Test Widget Helpers
class WidgetTestHelpers {
  static Widget createTestApp({Widget? child}) {
    return MaterialApp(
      home: child ?? Scaffold(body: Text('Test App')),
    );
  }

  static Widget createTestMaterialApp({Widget? child}) {
    return Material(
      child: child ?? Text('Test Widget'),
    );
  }

  static Future<void> pumpWidget(WidgetTester tester, Widget widget) async {
    await tester.pumpWidget(createTestApp(child: widget));
  }

  static Future<void> tapWidget(WidgetTester tester, Finder finder) async {
    await tester.tap(finder);
    await tester.pumpAndSettle();
  }

  static Future<void> enterText(
      WidgetTester tester, Finder finder, String text) async {
    await tester.enterText(finder, text);
    await tester.pumpAndSettle();
  }

  static Finder findWidgetByType(Type widgetType) {
    return find.byType(widgetType);
  }

  static Finder findWidgetByText(String text) {
    return find.text(text);
  }

  static Finder findWidgetByKey(Key key) {
    return find.byKey(key);
  }

  static Finder findWidgetWithIcon(IconData icon) {
    return find.byIcon(icon);
  }
}

// Test Validation Helpers
class ValidationTestHelpers {
  static bool isValidEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }

  static bool isValidPassword(String password) {
    // At least 8 characters, one uppercase, one lowercase, one number
    final passwordRegex =
        RegExp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d@$!%*?&]{8,}$');
    return passwordRegex.hasMatch(password);
  }

  static bool isValidPlantName(String name) {
    return name.isNotEmpty && name.length <= 100;
  }

  static bool isValidCultivarName(String name) {
    return name.isNotEmpty && name.length <= 100;
  }

  static bool isValidSensorValue(double value, String type) {
    switch (type) {
      case 'temperature':
        return value >= -50 && value <= 100;
      case 'humidity':
        return value >= 0 && value <= 100;
      case 'ph':
        return value >= 0 && value <= 14;
      case 'ec':
        return value >= 0 && value <= 10;
      case 'light':
        return value >= 0 && value <= 100000;
      default:
        return true;
    }
  }

  static bool isValidUsername(String username) {
    return username.isNotEmpty &&
        username.length >= 3 &&
        username.length <= 50 &&
        RegExp(r'^[a-zA-Z0-9_]+$').hasMatch(username);
  }
}

// Async Test Helpers
class AsyncTestHelpers {
  static Future<void> delay([int milliseconds = 100]) async {
    await Future.delayed(Duration(milliseconds: milliseconds));
  }

  static Future<void> waitForCondition(
    WidgetTester tester,
    bool Function() condition, {
    Duration timeout = const Duration(seconds: 5),
  }) async {
    final endTime = DateTime.now().add(timeout);
    while (DateTime.now().isBefore(endTime)) {
      await tester.pumpAndSettle();
      if (condition()) {
        return;
      }
      await delay(10);
    }
    throw Exception('Condition not met within timeout');
  }

  static Future<void> waitForWidget(
    WidgetTester tester,
    Finder finder, {
    Duration timeout = const Duration(seconds: 5),
  }) async {
    await waitForCondition(tester, () => finder.evaluate().isNotEmpty,
        timeout: timeout);
  }
}

// Test Environment Helpers
class TestEnvironmentHelpers {
  static void setUpTestEnvironment() {
    // Initialize test data
    MockApiClient.clearAll();

    // Add some test data
    MockApiClient.addCultivar(TestDataFactory.createTestCultivar(id: 1));
    MockApiClient.addCultivar(TestDataFactory.createTestCultivar(id: 2));
    MockApiClient.addPlant(TestDataFactory.createTestPlant());
    MockApiClient.addSensor(TestDataFactory.createTestSensor());
    MockApiClient.addUser(TestDataFactory.createTestUser());
    MockApiClient.addCartItem(TestDataFactory.createTestCartItem());
  }

  static void tearDownTestEnvironment() {
    MockApiClient.clearAll();
  }

  static void resetTestData() {
    MockApiClient.clearAll();
    setUpTestEnvironment();
  }
}

// Test Data Generators for Edge Cases
class EdgeCaseGenerators {
  static List<Plant> createEdgeCasePlants() {
    final now = DateTime.now();
    return [
      // Empty description
      TestDataFactory.createTestPlant(description: ''),

      // Very long description
      TestDataFactory.createTestPlant(description: 'a' * 1000),

      // Special characters
      TestDataFactory.createTestPlant(
          name: 'TestSpecialCharsAtHashDollarPercent'),

      // Unicode characters
      TestDataFactory.createTestPlant(name: 'Northern Lights Unicode'),

      // Null optional fields
      TestDataFactory.createTestPlant(
        cultivarId: null,
        harvestDate: null,
      ),

      // Very old plant (5+ years)
      TestDataFactory.createTestPlant(startDate: DateTime(2018, 1, 1)),

      // Future date (edge case)
      TestDataFactory.createTestPlant(startDate: DateTime(2025, 1, 1)),

      // Zero values
      TestDataFactory.createTestPlant(id: 0, statusId: 0),

      // Clone with autoflower
      TestDataFactory.createTestPlant(isClone: true, autoflower: true),
    ];
  }

  static List<cultivar_models.Cultivar> createEdgeCaseCultivars() {
    return [
      // Empty descriptions
      TestDataFactory.createTestCultivar(
        id: 1,
        name: 'Test Cultivar 1',
        description: '',
        shortDescription: '',
      ),

      // Very long descriptions
      TestDataFactory.createTestCultivar(
        id: 2,
        name: 'Test Cultivar 2',
        description: 'a' * 2000,
        shortDescription: 'a' * 500,
      ),

      // Zero values
      TestDataFactory.createTestCultivar(
        id: 3,
        name: 'Test Cultivar 3',
        indica: 0,
        sativa: 0,
        seedCount: 0,
      ),

      // Full values
      TestDataFactory.createTestCultivar(
        id: 4,
        name: 'Test Cultivar 4',
        indica: 100,
        sativa: 100,
        seedCount: 1000,
      ),

      // Extreme autoflower values
      TestDataFactory.createTestCultivar(
        id: 5,
        name: 'Test Cultivar 5',
        autoflower: true,
      ),

      // Special characters and Unicode
      TestDataFactory.createTestCultivar(
        id: 6,
        name: 'Test Cultivar 6',
      ),
    ];
  }

  static List<Sensor> createEdgeCaseSensors() {
    final now = DateTime.now();
    return [
      // Empty description
      TestDataFactory.createTestSensor(description: ''),

      // Very long description
      TestDataFactory.createTestSensor(description: 'a' * 1000),

      // Special characters
      TestDataFactory.createTestSensor(name: 'SensorAtHashDollarPercent'),

      // Extreme values
      TestDataFactory.createTestSensor(
        minValue: -50.0,
        maxValue: 100.0,
        lastValue: -25.0,
      ),

      // Boundary values
      TestDataFactory.createTestSensor(
        minValue: 0.0,
        maxValue: 0.0,
        lastValue: 0.0,
      ),

      // Future reading time
      TestDataFactory.createTestSensor(lastReading: DateTime(2025, 1, 1)),
    ];
  }

  static List<user_models.User> createEdgeCaseUsers() {
    final now = DateTime.now();
    return [
      // Empty optional fields
      TestDataFactory.createTestUser(
        firstName: '',
        lastName: '',
      ),

      // Very long names
      TestDataFactory.createTestUser(
        firstName: 'a' * 100,
        lastName: 'a' * 100,
      ),

      // Special characters
      TestDataFactory.createTestUser(
        username: 'test_user_123',
        email: 'test+tag@example.com',
      ),

      // Different roles
      TestDataFactory.createTestUser(role: user_models.UserRole.admin),
      TestDataFactory.createTestUser(role: user_models.UserRole.moderator),

      // Different statuses
      TestDataFactory.createTestUser(status: user_models.UserStatus.inactive),
      TestDataFactory.createTestUser(status: user_models.UserStatus.suspended),

      // Inactive user
      TestDataFactory.createTestUser(isActive: false),
    ];
  }
}

// Assertion Helpers for Better Test Readability
class TestAssertions {
  static void assertPlantValid(Plant plant, [String? message]) {
    expect(plant.id, greaterThan(0),
        reason: message ?? 'Plant ID should be positive');
    expect(plant.name, isNotEmpty,
        reason: message ?? 'Plant name should not be empty');
    expect(plant.statusId, greaterThan(0),
        reason: message ?? 'Plant status ID should be positive');
    expect(plant.userId, greaterThan(0),
        reason: message ?? 'Plant user ID should be positive');
  }

  static void assertCultivarValid(cultivar_models.Cultivar cultivar,
      [String? message]) {
    expect(cultivar.userId, greaterThan(0),
        reason: message ?? 'Cultivar user ID should be positive');
    expect(cultivar.name, isNotEmpty,
        reason: message ?? 'Cultivar name should not be empty');
    expect(cultivar.indica ?? 0, greaterThanOrEqualTo(0),
        reason: message ?? 'Indica percentage should be non-negative');
    expect(cultivar.sativa ?? 0, greaterThanOrEqualTo(0),
        reason: message ?? 'Sativa percentage should be non-negative');
    expect(cultivar.seedCount ?? 0, greaterThanOrEqualTo(0),
        reason: message ?? 'Seed count should be non-negative');
  }

  static void assertSensorValid(Sensor sensor, [String? message]) {
    expect(sensor.id, greaterThan(0),
        reason: message ?? 'Sensor ID should be positive');
    expect(sensor.name, isNotEmpty,
        reason: message ?? 'Sensor name should not be empty');
    expect(sensor.type, isNotEmpty,
        reason: message ?? 'Sensor type should not be empty');
    expect(sensor.model, isNotEmpty,
        reason: message ?? 'Sensor model should not be empty');
  }

  static void assertUserValid(user_models.User user, [String? message]) {
    expect(user.id, greaterThan(0),
        reason: message ?? 'User ID should be positive');
    expect(user.username, isNotEmpty,
        reason: message ?? 'Username should not be empty');
    expect(user.email, isNotEmpty,
        reason: message ?? 'Email should not be empty');
    expect(user.email, contains('@'),
        reason: message ?? 'Email should contain @ symbol');
  }

  static void assertAuthUserValid(auth_models.User user, [String? message]) {
    expect(user.id, greaterThan(0),
        reason: message ?? 'Auth User ID should be positive');
    expect(user.username, isNotEmpty,
        reason: message ?? 'Auth Username should not be empty');
    expect(user.email, isNotEmpty,
        reason: message ?? 'Auth Email should not be empty');
    expect(user.email, contains('@'),
        reason: message ?? 'Auth Email should contain @ symbol');
  }
}
