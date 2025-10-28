// API service for cultivars management

import 'dart:convert';
import 'dart:io';
import 'dart:math';
import '../core/logging.dart';
import '../models/cultivar.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:5002';
  static const String cultivarsEndpoint = '/cultivars';
  static const String apiEndpoint = '$cultivarsEndpoint/api';

  // Store authentication token
  static String? _authToken;
  static String? _userEmail;

  // Mock user ID for demo purposes
  static const int _mockUserId = 1;

  static void setAuthToken(String token, String email) {
    _authToken = token;
    _userEmail = email;
  }

  static void clearAuth() {
    _authToken = null;
    _userEmail = null;
  }

  // Build headers with authentication
  static Map<String, String> _buildHeaders() {
    final headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (_authToken != null) {
      headers['Authorization'] = 'Bearer $_authToken';
    }

    return headers;
  }

  // Make HTTP request using HttpClient
  static Future<String> _makeRequest(
    String method,
    String url,
    Map<String, dynamic>? body,
  ) async {
    try {
      final client = HttpClient();
      final request = await client.openUrl(method, Uri.parse(url));
      
      // Add headers
      _buildHeaders().forEach((key, value) {
        request.headers.set(key, value);
      });

      // Add body for POST/PUT requests
      if (body != null) {
        request.write(json.encode(body));
      }

      final response = await request.close();
      final responseBody = await response.transform(utf8.decoder).join();

      if (response.statusCode >= 200 && response.statusCode < 300) {
        return responseBody;
      } else {
        throw _handleErrorResponse(response.statusCode, responseBody);
      }
    } on SocketException {
      throw Exception('Network error. Please check your connection.');
    } on HttpException {
      throw Exception('Server error. Please try again later.');
    } catch (e) {
      throw Exception('Unexpected error: $e');
    }
  }

  // Handle error responses
  static Exception _handleErrorResponse(int statusCode, String responseBody) {
    try {
      final jsonResponse = json.decode(responseBody);
      final message = jsonResponse['message'] ?? jsonResponse['error'] ?? 'Unknown error';
      return Exception(message);
    } catch (e) {
      switch (statusCode) {
        case 401:
          return Exception('Authentication required');
        case 403:
          return Exception('Access denied');
        case 404:
          return Exception('Resource not found');
        case 500:
          return Exception('Server error');
        default:
          return Exception('HTTP $statusCode error');
      }
    }
  }

  // GET /api/cultivars/list - Get list of cultivars
  static Future<List<Cultivar>> getCultivars() async {
    try {
      final responseBody = await _makeRequest('GET', '$baseUrl$apiEndpoint/list', null);
      final jsonResponse = json.decode(responseBody);
      
      if (jsonResponse is Map && jsonResponse.containsKey('data')) {
        final data = jsonResponse['data'];
        if (data is List) {
          return data.map((item) => Cultivar.fromJson(item)).toList();
        }
      }
      
      // Fallback to mock data for development
      return MockData.getMockCultivars();
    } catch (e) {
  // Return mock data if API fails
  AppLogger.error('API call failed, using mock data', e);
      return MockData.getMockCultivars();
    }
  }

  // GET /api/cultivars/{id} - Get single cultivar
  static Future<Cultivar> getCultivar(int id) async {
    try {
      final responseBody = await _makeRequest('GET', '$baseUrl$apiEndpoint/$id', null);
      final jsonResponse = json.decode(responseBody);
      
      if (jsonResponse is Map && jsonResponse.containsKey('data')) {
        return Cultivar.fromJson(jsonResponse['data']);
      } else {
        return Cultivar.fromJson(jsonResponse);
      }
    } catch (e) {
  // Return mock data if API fails
  AppLogger.error('API call failed, using mock data', e);
      final mockData = MockData.getMockCultivars();
      return mockData.firstWhere(
        (cultivar) => cultivar.id == id,
        orElse: () => mockData.first,
      );
    }
  }

  // POST /api/cultivars/create - Create new cultivar
  static Future<Cultivar> createCultivar({
    required String name,
    String? description,
    String? shortDescription,
    int? breederId,
    int indica = 50,
    int sativa = 50,
    bool autoflower = false,
    int seedCount = 0,
    int? cycleTime,
    String? url,
  }) async {
    final data = {
      'name': name,
      'description': description,
      'short_description': shortDescription,
      'breeder_id': breederId,
      'indica': indica,
      'sativa': sativa,
      'autoflower': autoflower,
      'seed_count': seedCount,
      'cycle_time': cycleTime,
      'url': url,
      'user_id': _mockUserId, // Add user_id for demo
    };

    try {
      final responseBody = await _makeRequest('POST', '$baseUrl$apiEndpoint/create', data);
      final jsonResponse = json.decode(responseBody);
      
      if (jsonResponse is Map && jsonResponse.containsKey('data')) {
        return Cultivar.fromJson(jsonResponse['data']);
      } else {
        return Cultivar.fromJson(jsonResponse);
      }
    } catch (e) {
  // Return mock data if API fails
  AppLogger.error('API call failed, creating mock cultivar', e);
      
      // Create a mock cultivar with a random ID
      final randomId = Random().nextInt(1000) + 100;
      return Cultivar(
        id: randomId,
        userId: _mockUserId,
        name: name,
        breederId: breederId,
        breederName: 'Unknown Breeder',
        indica: indica,
        sativa: sativa,
        autoflower: autoflower,
        description: description,
        shortDescription: shortDescription,
        seedCount: seedCount,
        cycleTime: cycleTime,
        url: url,
      );
    }
  }

  // PUT /api/cultivars/{id} - Update cultivar
  static Future<Cultivar> updateCultivar(
    int id, {
    String? name,
    String? description,
    String? shortDescription,
    int? breederId,
    int? indica,
    int? sativa,
    bool? autoflower,
    int? seedCount,
    int? cycleTime,
    String? url,
  }) async {
    final data = <String, dynamic>{};
    if (name != null) data['name'] = name;
    if (description != null) data['description'] = description;
    if (shortDescription != null) data['short_description'] = shortDescription;
    if (breederId != null) data['breeder_id'] = breederId;
    if (indica != null) data['indica'] = indica;
    if (sativa != null) data['sativa'] = sativa;
    if (autoflower != null) data['autoflower'] = autoflower;
    if (seedCount != null) data['seed_count'] = seedCount;
    if (cycleTime != null) data['cycle_time'] = cycleTime;
    if (url != null) data['url'] = url;

    try {
      final responseBody = await _makeRequest('PUT', '$baseUrl$apiEndpoint/$id', data);
      final jsonResponse = json.decode(responseBody);
      
      if (jsonResponse is Map && jsonResponse.containsKey('data')) {
        return Cultivar.fromJson(jsonResponse['data']);
      } else {
        return Cultivar.fromJson(jsonResponse);
      }
    } catch (e) {
  // Return mock data if API fails
  AppLogger.error('API call failed, updating mock cultivar', e);
      
      // Return the original cultivar with updated fields
      final mockData = MockData.getMockCultivars();
      final originalCultivar = mockData.firstWhere(
        (cultivar) => cultivar.id == id,
        orElse: () => mockData.first,
      );
      
      return originalCultivar.copyWith(
        name: name,
        description: description,
        shortDescription: shortDescription,
        breederId: breederId,
        indica: indica,
        sativa: sativa,
        autoflower: autoflower,
        seedCount: seedCount,
        cycleTime: cycleTime,
        url: url,
      );
    }
  }

  // DELETE /api/cultivars/{id} - Delete cultivar
  static Future<void> deleteCultivar(int id) async {
    try {
      await _makeRequest('DELETE', '$baseUrl$apiEndpoint/$id', null);
    } catch (e) {
  // Log but don't throw for mock data
  AppLogger.error('API call failed', e);
    }
  }

  // GET /api/cultivars/stats - Get cultivar statistics
  static Future<CultivarStats> getCultivarStats() async {
    try {
      final responseBody = await _makeRequest('GET', '$baseUrl$apiEndpoint/stats', null);
      final jsonResponse = json.decode(responseBody);
      
      if (jsonResponse is Map && jsonResponse.containsKey('data')) {
        return CultivarStats.fromJson(jsonResponse['data']);
      } else {
        return CultivarStats.fromJson(jsonResponse);
      }
    } catch (e) {
  // Return mock data if API fails
  AppLogger.error('API call failed, using mock stats', e);
      return MockData.getMockStats();
    }
  }

  // Mock authentication methods for demo
  static Future<bool> login(String email, String password) async {
    // Simulate API call delay
    await Future.delayed(const Duration(seconds: 1));
    
    // Mock successful login (in real app, this would call backend API)
    if (email.isNotEmpty && password.isNotEmpty) {
      setAuthToken('mock_token_123', email);
      return true;
    }
    return false;
  }

  static Future<bool> signup(String email, String password, String name) async {
    // Simulate API call delay
    await Future.delayed(const Duration(seconds: 1));
    
    // Mock successful signup
    if (email.isNotEmpty && password.isNotEmpty && name.isNotEmpty) {
      setAuthToken('mock_token_123', email);
      return true;
    }
    return false;
  }

  static void logout() {
    clearAuth();
  }

  static bool get isAuthenticated => _authToken != null;
  static String? get currentUserEmail => _userEmail;
}

// Mock data for development/demo
class MockData {
  static List<Cultivar> getMockCultivars() {
    return [
      Cultivar(
        id: 1,
        userId: 1,
        name: 'White Widow',
        breederName: 'Green House Seeds',
        indica: 60,
        sativa: 40,
        autoflower: false,
        description: 'Classic indica-dominant hybrid with balanced effects',
        shortDescription: 'Classic hybrid with resinous buds',
        seedCount: 10,
        cycleTime: 60,
        plantCount: 3,
      ),
      Cultivar(
        id: 2,
        userId: 1,
        name: 'Northern Lights Auto',
        breederName: 'Sensi Seeds',
        indica: 80,
        sativa: 20,
        autoflower: true,
        description: 'Pure indica with relaxing effects, autoflowering variety',
        shortDescription: 'Autoflower indica with strong effects',
        seedCount: 5,
        cycleTime: 70,
        plantCount: 2,
      ),
      Cultivar(
        id: 3,
        userId: 1,
        name: 'Blue Dream',
        breederName: 'California Genetics',
        indica: 20,
        sativa: 80,
        autoflower: false,
        description: 'Sativa-dominant hybrid with sweet berry aroma',
        shortDescription: 'Sweet, uplifting sativa-dominant strain',
        seedCount: 8,
        cycleTime: 65,
        plantCount: 1,
      ),
    ];
  }

  static CultivarStats getMockStats() {
    return CultivarStats(
      totalCultivars: 3,
      autoflower: 1,
      photoperiod: 2,
      mostUsedCultivar: 'White Widow',
      mostUsedCount: 3,
    );
  }
}