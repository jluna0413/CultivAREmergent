// lib/core/services/api_client.dart

import 'dart:math';

import '../models/auth_models.dart';
import '../models/plant_models.dart';
import '../models/cultivar_models.dart';
import '../models/sensor_models.dart';
import '../models/dashboard_stats.dart';
import '../models/product_models.dart' hide CartItem;
import '../models/cart_models.dart' hide Product;

class ApiClient {
  // Token management
  String? _authToken;

  /// Set authentication token for API requests
  void setAuthToken(String token) {
    _authToken = token;
  }

  /// Clear authentication token
  void clearAuthToken() {
    _authToken = null;
  }

  /// Get current authentication token
  String? get authToken => _authToken;

  // Placeholder for API client methods
  Future<Map<String, dynamic>> get(
    String? path, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? queryParams,
  }) async {
    // Accept both queryParameters and queryParams for compatibility with call sites
    final qp = queryParameters ?? queryParams;
    await Future.delayed(const Duration(milliseconds: 200));
    return {
      'message': 'GET request to $path successful',
      if (qp != null) 'query': qp,
    };
  }

  Future<Map<String, dynamic>> post(
    String? path,
    Map<String, dynamic> data, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? queryParams,
  }) async {
    final qp = queryParameters ?? queryParams;
    await Future.delayed(const Duration(milliseconds: 200));
    return {
      'message': 'POST request to $path successful',
      'data': data,
      if (qp != null) 'query': qp,
    };
  }

  Future<Map<String, dynamic>> put(
    String? path,
    Map<String, dynamic> data, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? queryParams,
  }) async {
    final qp = queryParameters ?? queryParams;
    await Future.delayed(const Duration(milliseconds: 200));
    return {
      'message': 'PUT request to $path successful',
      'data': data,
      if (qp != null) 'query': qp,
    };
  }

  Future<void> delete(
    String? path, {
    Map<String, dynamic>? queryParameters,
    Map<String, dynamic>? queryParams,
  }) async {
    // Accept both queryParameters and queryParams for backward compatibility.
    await Future.delayed(const Duration(milliseconds: 200));
    return Future.value();
  }

  Future<AuthResponse> login(String email, String password) async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _mockAuthResponse(email: email);
  }

  Future<AuthResponse> register({
    required String username,
    required String email,
    required String password,
  }) async {
    await Future.delayed(const Duration(milliseconds: 300));
    return _mockAuthResponse(email: email, username: username);
  }

  Future<void> logout() async {
    await Future.delayed(const Duration(milliseconds: 150));
  }

  Future<AuthResponse> refreshToken(String refreshToken) async {
    await Future.delayed(const Duration(milliseconds: 250));
    return _mockAuthResponse(email: 'user@example.com');
  }

  AuthResponse _mockAuthResponse({required String email, String? username}) {
    final now = DateTime.now();
    final id = Random().nextInt(10000);
    return AuthResponse(
      accessToken: 'access_$id',
      tokenType: 'bearer',
      refreshToken: 'refresh_$id',
      user: User(
        id: id,
        email: email,
        username: username ?? email.split('@').first,
        avatar: null,
        createdAt: now,
        updatedAt: now,
      ),
    );
  }

  // Plants API methods
  Future<List<PlantModel>> getPlants() async {
    await Future.delayed(const Duration(milliseconds: 250));

    final List<PlantModel> plants = [];

    for (int i = 1; i <= 5; i++) {
      plants.add(
        PlantModel(
          id: i,
          name: 'Plant $i',
          description: 'Description for plant $i',
          statusId: i % 3 == 0 ? 3 : 2, // Mix of flowering and vegetative
          cultivarId: i % 2 == 0 ? 1 : 2, // Mix of cultivars
          isClone: i % 2 == 0,
          autoflower: false,
          startDate: DateTime.now().subtract(Duration(days: i * 10)),
          lastWaterDate: DateTime.now().subtract(Duration(hours: i * 2)),
          lastFeedDate: DateTime.now().subtract(Duration(days: i)),
          harvestDate: null,
          userId: 1,
          createdAt: DateTime.now().subtract(Duration(days: i * 15)),
          updatedAt: DateTime.now(),
        ),
      );
    }

    return plants;
  }

  Future<PlantModel> getPlant(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return PlantModel(
      id: id,
      name: 'Plant $id',
      description: 'Description for plant $id',
      statusId: 2,
      cultivarId: 1,
      isClone: false,
      autoflower: false,
      startDate: DateTime.now().subtract(const Duration(days: 30)),
      lastWaterDate: DateTime.now().subtract(const Duration(hours: 2)),
      lastFeedDate: DateTime.now().subtract(const Duration(days: 1)),
      harvestDate: null,
      userId: 1,
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now(),
    );
  }

  Future<PlantModel> createPlant(PlantCreateModel request) async {
    await Future.delayed(const Duration(milliseconds: 300));
    return PlantModel(
      id: DateTime.now().millisecondsSinceEpoch,
      name: request.name,
      description: request.description ?? '',
      statusId: request.statusId,
      cultivarId: request.cultivarId ?? 1,
      isClone: request.isClone,
      autoflower: request.autoflower,
      startDate: DateTime.now(),
      lastWaterDate: null,
      lastFeedDate: null,
      harvestDate: null,
      userId: 1,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  Future<PlantModel> updatePlant(int id, PlantUpdateModel request) async {
    await Future.delayed(const Duration(milliseconds: 250));
    return PlantModel(
      id: id,
      name: request.name ?? 'Updated Plant',
      description: request.description ?? 'Updated description',
      statusId: request.statusId ?? 2,
      cultivarId: request.cultivarId ?? 1,
      isClone: request.isClone ?? false,
      autoflower: request.autoflower ?? false,
      startDate: request.startDate ?? DateTime.now(),
      lastWaterDate: request.lastWaterDate,
      lastFeedDate: request.lastFeedDate,
      harvestDate: request.harvestDate,
      userId: 1,
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now(),
    );
  }

  Future<void> deletePlant(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return Future.value();
  }

  // Cultivars API methods
  Future<List<Cultivar>> getCultivars() async {
    await Future.delayed(const Duration(milliseconds: 250));

    final List<Cultivar> cultivars = [];

    for (int i = 1; i <= 3; i++) {
      cultivars.add(
        Cultivar(
          id: i,
          name: i == 1
              ? 'OG Kush'
              : i == 2
              ? 'Blue Dream'
              : 'White Widow',
          description: 'Description for cultivar $i',
          genetics: 'Genetic information for cultivar $i',
          thcContent: 15.0 + i,
          cbdContent: 1.0 + (i * 0.1),
          breederId: 1,
          isActive: true,
          createdAt: DateTime.now().subtract(Duration(days: i * 20)),
          updatedAt: DateTime.now(),
          effects: 'relaxing, euphoric',
          flavor: 'sweet',
        ),
      );
    }

    return cultivars;
  }

  // Sensor API methods - return proper Sensor objects
  Future<List<Sensor>> getAllSensors() async {
    await Future.delayed(const Duration(milliseconds: 250));

    final List<Sensor> sensors = [];

    for (int i = 1; i <= 5; i++) {
      sensors.add(
        Sensor(
          id: i,
          name: 'Sensor $i',
          description: 'Description for sensor $i',
          type: i % 2 == 0 ? 'humidity' : 'temperature',
          model: 'Model X$i',
          location: 'Grow Tent ${String.fromCharCode(65 + (i % 3))}',
          zone: 'Zone $i',
          status: i % 4 == 0 ? SensorStatus.offline : SensorStatus.online,
          apiEndpoint: 'http://sensor$i.local/api',
          apiKey: 'key_$i',
          unit: i % 2 == 0 ? '%' : '°C',
          minThreshold: i % 2 == 0 ? 40.0 : 18.0,
          maxThreshold: i % 2 == 0 ? 70.0 : 30.0,
          isActive: true,
          lastReading: DateTime.now().subtract(Duration(minutes: i * 5)),
          value: i % 2 == 0 ? 65.0 + i : 22.5 + i,
          health: i % 5 == 0 ? SensorHealth.warning : SensorHealth.good,
          firmware: 'v1.$i.0',
          createdAt: DateTime.now().subtract(Duration(days: i * 10)),
          updatedAt: DateTime.now(),
        ),
      );
    }

    return sensors;
  }

  Future<Sensor> getSensorById(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return Sensor(
      id: id,
      name: 'Sensor $id',
      description: 'Description for sensor $id',
      type: id % 2 == 0 ? 'humidity' : 'temperature',
      model: 'Model X$id',
      location: 'Grow Tent A',
      zone: 'Zone $id',
      status: SensorStatus.online,
      apiEndpoint: 'http://sensor$id.local/api',
      apiKey: 'key_$id',
      unit: id % 2 == 0 ? '%' : '°C',
      minThreshold: id % 2 == 0 ? 40.0 : 18.0,
      maxThreshold: id % 2 == 0 ? 70.0 : 30.0,
      isActive: true,
      lastReading: DateTime.now().subtract(Duration(minutes: id * 5)),
      value: id % 2 == 0 ? 65.0 + id : 22.5 + id,
      health: SensorHealth.good,
      firmware: 'v1.$id.0',
      createdAt: DateTime.now().subtract(Duration(days: id * 10)),
      updatedAt: DateTime.now(),
    );
  }

  Future<Sensor> createSensor(dynamic sensorData) async {
    await Future.delayed(const Duration(milliseconds: 300));
    final int newId = DateTime.now().millisecondsSinceEpoch;

    // Extract and cast values with safe defaults
    final dataMap = sensorData as Map<String, dynamic>;

    return Sensor(
      id: newId,
      name: dataMap['name'] as String? ?? 'New Sensor',
      description: dataMap['description'] as String?,
      type: dataMap['type'] as String? ?? 'temperature',
      model: dataMap['model'] as String? ?? 'Unknown Model',
      location: dataMap['location'] as String?,
      zone: dataMap['zone'] as String?,
      status: SensorStatus.online,
      apiEndpoint: dataMap['api_endpoint'] as String?,
      apiKey: dataMap['api_key'] as String?,
      unit: dataMap['unit'] as String?,
      minThreshold: (dataMap['min_threshold'] as num?)?.toDouble(),
      maxThreshold: (dataMap['max_threshold'] as num?)?.toDouble(),
      isActive: dataMap['is_active'] as bool? ?? true,
      lastReading: DateTime.now(),
      value: 0.0,
      health: SensorHealth.good,
      firmware: 'v1.0.0',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  Future<Sensor> updateSensor(int id, dynamic sensorData) async {
    await Future.delayed(const Duration(milliseconds: 250));

    // Extract and cast values with safe defaults
    final dataMap = sensorData as Map<String, dynamic>;

    return Sensor(
      id: id,
      name: dataMap['name'] as String? ?? 'Updated Sensor',
      description: dataMap['description'] as String?,
      type: dataMap['type'] as String? ?? 'temperature',
      model: dataMap['model'] as String? ?? 'Unknown Model',
      location: dataMap['location'] as String?,
      zone: dataMap['zone'] as String?,
      status: _parseStatus(dataMap['status'] as String? ?? 'online'),
      apiEndpoint: dataMap['api_endpoint'] as String?,
      apiKey: dataMap['api_key'] as String?,
      unit: dataMap['unit'] as String?,
      minThreshold: (dataMap['min_threshold'] as num?)?.toDouble(),
      maxThreshold: (dataMap['max_threshold'] as num?)?.toDouble(),
      isActive: dataMap['is_active'] as bool? ?? true,
      lastReading: DateTime.now(),
      value: 25.0,
      health: SensorHealth.good,
      firmware: 'v1.0.0',
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now(),
    );
  }

  Future<void> deleteSensor(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return Future.value();
  }

  // Helper method to parse status string to SensorStatus enum
  SensorStatus _parseStatus(String statusStr) {
    switch (statusStr.toLowerCase()) {
      case 'online':
        return SensorStatus.online;
      case 'offline':
        return SensorStatus.offline;
      case 'calibrating':
        return SensorStatus.calibrating;
      case 'error':
        return SensorStatus.error;
      case 'maintenance':
        return SensorStatus.maintenance;
      default:
        return SensorStatus.offline;
    }
  }

  // Legacy methods for backward compatibility - return maps with nested data
  Future<Map<String, dynamic>> getSensors() async {
    final sensors = await getAllSensors();
    return {'sensors': sensors.map((sensor) => sensor.toJson()).toList()};
  }

  Future<Map<String, dynamic>> getSensor(String id) async {
    final sensor = await getSensorById(int.parse(id));
    return {'sensor': sensor.toJson()};
  }

  Future<Map<String, dynamic>> createSensorData(
    Map<String, dynamic> sensorData,
  ) async {
    final sensor = await createSensor(sensorData);
    return {'sensor': sensor.toJson()};
  }

  Future<Map<String, dynamic>> updateSensorData(
    String id,
    Map<String, dynamic> sensorData,
  ) async {
    final sensor = await updateSensor(int.parse(id), sensorData);
    return {'sensor': sensor.toJson()};
  }

  // Dashboard API methods
  Future<DashboardStats> getDashboardStats() async {
    await Future.delayed(const Duration(milliseconds: 300));
    return DashboardStats(
      counts: const CountStats(
        total: 15,
        active: 12,
        harvested: 3,
        seedlings: 2,
        vegetative: 6,
        flowering: 4,
      ),
      cultivars: const CultivarStats(totalCultivars: 5, userCultivars: 3),
      environment: const EnvironmentalStats(
        avgTemperature: 24.5,
        avgHumidity: 65.0,
        avgPh: 6.2,
        avgEc: 1.8,
      ),
      sensors: SensorStats(
        totalSensors: 8,
        activeSensors: 7,
        lastReadingTime: DateTime.now(),
      ),
      dataSlices: const EnvironmentalSlice(
        temperatureData: [],
        humidityData: [],
        phData: [],
        ecData: [],
      ),
      generatedAt: DateTime.now(),
      userId: 1,
    );
  }

  // Cart and Product API methods for cache sync service
  Future<List<CartItem>> getCartItems() async {
    await Future.delayed(const Duration(milliseconds: 200));

    final List<CartItem> cartItems = [];

    for (int i = 1; i <= 3; i++) {
      cartItems.add(
        CartItem(
          id: i,
          productId: i,
          productName: 'Product $i',
          price: 29.99 * i,
          quantity: i + 1,
          description: 'Description for product $i',
          productData: {'variant': 'variant_$i'},
          createdAt: DateTime.now().subtract(Duration(days: i)),
          updatedAt: DateTime.now(),
        ),
      );
    }

    return cartItems;
  }

  Future<List<Product>> getProducts() async {
    await Future.delayed(const Duration(milliseconds: 250));

    final List<Product> products = [];

    for (int i = 1; i <= 5; i++) {
      products.add(
        Product(
          id: i,
          name: 'Product $i',
          description: 'Description for product $i',
          price: 29.99 + i,
          category: ProductCategory.seed,
          inStock: true,
          imageUrl: 'https://example.com/product$i.jpg',
        ),
      );
    }

    return products;
  }

  // Cultivar API methods for direct operations
  Future<Cultivar> getCultivar(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return Cultivar(
      id: id,
      name: 'Cultivar $id',
      description: 'Description for cultivar $id',
      genetics: 'Genetic information for cultivar $id',
      thcContent: 15.0 + id,
      cbdContent: 1.0 + (id * 0.1),
      breederId: 1,
      isActive: true,
      createdAt: DateTime.now().subtract(Duration(days: id * 20)),
      updatedAt: DateTime.now(),
      effects: 'relaxing, euphoric',
      flavor: 'sweet',
    );
  }

  Future<Cultivar> createCultivar(dynamic cultivarData) async {
    await Future.delayed(const Duration(milliseconds: 300));
    final int newId = DateTime.now().millisecondsSinceEpoch;

    // Extract and cast values with safe defaults
    final dataMap = cultivarData as Map<String, dynamic>;

    return Cultivar(
      id: newId,
      name: dataMap['name'] as String? ?? 'New Cultivar',
      description: dataMap['description'] as String?,
      genetics: dataMap['genetics'] as String? ?? '',
      thcContent: (dataMap['thc_content'] as num?)?.toDouble() ?? 15.0,
      cbdContent: (dataMap['cbd_content'] as num?)?.toDouble() ?? 1.0,
      breederId: dataMap['breeder_id'] as int? ?? 1,
      isActive: dataMap['is_active'] as bool? ?? true,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
      effects: dataMap['effects'] as String?,
      flavor: dataMap['flavor'] as String?,
    );
  }

  Future<Cultivar> updateCultivar(int id, dynamic cultivarData) async {
    await Future.delayed(const Duration(milliseconds: 250));

    // Extract and cast values with safe defaults
    final dataMap = cultivarData as Map<String, dynamic>;

    return Cultivar(
      id: id,
      name: dataMap['name'] as String? ?? 'Updated Cultivar',
      description: dataMap['description'] as String?,
      genetics: dataMap['genetics'] as String? ?? '',
      thcContent: (dataMap['thc_content'] as num?)?.toDouble() ?? 15.0,
      cbdContent: (dataMap['cbd_content'] as num?)?.toDouble() ?? 1.0,
      breederId: dataMap['breeder_id'] as int? ?? 1,
      isActive: dataMap['is_active'] as bool? ?? true,
      createdAt: DateTime.now().subtract(const Duration(days: 30)),
      updatedAt: DateTime.now(),
      effects: dataMap['effects'] as String?,
      flavor: dataMap['flavor'] as String?,
    );
  }

  Future<void> deleteCultivar(int id) async {
    await Future.delayed(const Duration(milliseconds: 200));
    return Future.value();
  }

  // Add pagination support for cache sync service
  Future<Map<String, dynamic>> getProductsPaginated({
    int page = 1,
    int pageSize = 10,
  }) async {
    await Future.delayed(const Duration(milliseconds: 250));

    final List<Product> products = [];

    for (int i = 1; i <= pageSize; i++) {
      final int id = (page - 1) * pageSize + i;
      products.add(
        Product(
          id: id,
          name: 'Product $id',
          description: 'Description for product $id',
          price: 29.99 + id,
          category: ProductCategory.values[id % ProductCategory.values.length],
          inStock: true,
          imageUrl: 'https://example.com/product$id.jpg',
        ),
      );
    }

    return {
      'products': products
          .map(
            (p) => {
              'id': p.id,
              'name': p.name,
              'description': p.description,
              'price': p.price,
              'category': p.category.name,
              'in_stock': p.inStock,
              'image_url': p.imageUrl,
            },
          )
          .toList(),
      'page': page,
      'page_size': pageSize,
    };
  }
}

class ApiException implements Exception {
  ApiException(this.message, {this.statusCode});
  final String message;
  final int? statusCode;

  @override
  String toString() {
    if (statusCode != null) {
      return 'ApiException: Status Code $statusCode - $message';
    }
    return 'ApiException: $message';
  }
}
