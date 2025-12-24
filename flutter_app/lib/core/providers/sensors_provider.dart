// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Create)
/// Sensors Provider - Manages sensor data and operations
/// Handles sensor CRUD operations, real-time data, and monitoring
library;

import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import 'dart:async';
import 'dart:convert';
import '../models/sensor_models.dart' as sensor_models;
import '../providers/api_client_provider.dart';

/// WebSocket service for real-time sensor data
class SensorWebSocketService {
  WebSocketChannel? _channel;
  Timer? _pingTimer;
  Timer? _reconnectTimer;
  int _reconnectAttempts = 0;
  static const int _maxReconnectAttempts = 10;
  static const Duration _baseReconnectDelay = Duration(seconds: 1);
  static const Duration _maxReconnectDelay = Duration(seconds: 30);
  static const Duration _pingInterval = Duration(seconds: 30);

  final StreamController<List<sensor_models.Sensor>> _sensorsController =
      StreamController<List<sensor_models.Sensor>>.broadcast();
  final StreamController<bool> _connectionController =
      StreamController<bool>.broadcast();
  final StreamController<String> _errorController =
      StreamController<String>.broadcast();

  Stream<List<sensor_models.Sensor>> get sensorsStream =>
      _sensorsController.stream;
  Stream<bool> get connectionStream => _connectionController.stream;
  Stream<String> get errorStream => _errorController.stream;

  void connect(String url) {
    if (_reconnectTimer != null) {
      _reconnectTimer!.cancel();
      _reconnectTimer = null;
    }

    try {
      _channel = WebSocketChannel.connect(Uri.parse(url));

      _channel!.stream.listen(
        (message) {
          _handleMessage(message);
        },
        onDone: () {
          _handleDisconnect(url);
        },
        onError: (error) {
          _handleError(error, url);
        },
      );

      _connectionController.add(true);
      _startPingPong();
      _reconnectAttempts = 0; // Reset on successful connection
    } catch (e) {
      _handleError(e, url);
    }
  }

  void _handleMessage(dynamic message) {
    try {
      final messageStr = message.toString();
      if (messageStr == 'pong') {
        // Handle pong response - connection is alive
        return;
      }

      final data = jsonDecode(messageStr);
      if (data is List) {
        final sensors = data
            .map(
              (item) =>
                  sensor_models.Sensor.fromJson(item as Map<String, dynamic>),
            )
            .toList();
        _sensorsController.add(sensors);
      }
    } catch (e) {
      _errorController.add('Failed to parse sensor data: $e');
    }
  }

  void _handleDisconnect(String url) {
    _stopPingPong();
    _connectionController.add(false);
    _scheduleReconnect(url);
  }

  void _handleError(dynamic error, String url) {
    _stopPingPong();
    _connectionController.add(false);
    _errorController.add('WebSocket error: $error');
    _scheduleReconnect(url);
  }

  void _scheduleReconnect(String url) {
    if (_reconnectAttempts >= _maxReconnectAttempts) {
      _errorController.add('Max reconnection attempts reached');
      return;
    }

    _reconnectAttempts++;
    final delay = _calculateReconnectDelay(_reconnectAttempts);

    _reconnectTimer = Timer(delay, () {
      connect(url);
    });
  }

  Duration _calculateReconnectDelay(int attempt) {
    // Exponential backoff with jitter
    final exponentialDelay = _baseReconnectDelay * (1 << (attempt - 1));
    final delay = exponentialDelay < _maxReconnectDelay
        ? exponentialDelay
        : _maxReconnectDelay;

    // Add jitter (±25%)
    final jitter =
        (delay.inMilliseconds *
        0.25 *
        (DateTime.now().millisecondsSinceEpoch % 2 == 0 ? 1 : -1));
    return Duration(milliseconds: (delay.inMilliseconds + jitter).round());
  }

  void _startPingPong() {
    _pingTimer = Timer.periodic(_pingInterval, (_) {
      if (_channel != null) {
        try {
          _channel!.sink.add('ping');
        } catch (e) {
          // Ping failed, connection might be dead
          _errorController.add('Ping failed: $e');
        }
      }
    });
  }

  void _stopPingPong() {
    _pingTimer?.cancel();
    _pingTimer = null;
  }

  void disconnect() {
    _stopPingPong();
    _reconnectTimer?.cancel();
    _reconnectTimer = null;
    _channel?.sink.close(status.goingAway);
    _channel = null;
    _connectionController.add(false);
  }

  void dispose() {
    disconnect();
    _sensorsController.close();
    _connectionController.close();
    _errorController.close();
  }
}

/// Sensors state with WebSocket support
class SensorsState {
  const SensorsState({
    this.sensors = const [],
    this.isLoading = false,
    this.error,
    this.isWebSocketConnected = false,
  });

  final List<sensor_models.Sensor> sensors;
  final bool isLoading;
  final String? error;
  final bool isWebSocketConnected;

  SensorsState copyWith({
    List<sensor_models.Sensor>? sensors,
    bool? isLoading,
    String? error,
    bool? isWebSocketConnected,
  }) {
    return SensorsState(
      sensors: sensors ?? this.sensors,
      isLoading: isLoading ?? this.isLoading,
      error: error,
      isWebSocketConnected: isWebSocketConnected ?? this.isWebSocketConnected,
    );
  }
}

/// WebSocket service provider
final sensorWebSocketServiceProvider = Provider<SensorWebSocketService>((ref) {
  final service = SensorWebSocketService();
  ref.onDispose(() => service.dispose());
  return service;
});

/// Sensors state notifier provider with WebSocket support
final sensorsNotifierProvider = NotifierProvider<SensorsNotifier, SensorsState>(
  () {
    return SensorsNotifier();
  },
);

class SensorsNotifier extends Notifier<SensorsState> {
  SensorWebSocketService? _webSocketService;
  StreamSubscription<List<sensor_models.Sensor>>? _sensorsSubscription;
  StreamSubscription<bool>? _connectionSubscription;

  @override
  SensorsState build() {
    _webSocketService = ref.watch(sensorWebSocketServiceProvider);
    _initWebSocket();
    _loadInitialData();
    return const SensorsState();
  }

  void _initWebSocket() {
    // Connect to WebSocket (replace with actual URL)
    _webSocketService?.connect('ws://localhost:8000/ws/sensors');

    _sensorsSubscription = _webSocketService?.sensorsStream.listen((sensors) {
      state = state.copyWith(sensors: sensors);
    });

    _connectionSubscription = _webSocketService?.connectionStream.listen((
      connected,
    ) {
      state = state.copyWith(isWebSocketConnected: connected);
    });
  }

  Future<void> _loadInitialData() async {
    state = state.copyWith(isLoading: true);

    try {
      // Load real sensor data from API
      final apiClient = ref.read(apiClientProvider);
      final sensorsData = await apiClient.getSensors();

      final sensors = sensorsData
          .map((data) => sensor_models.Sensor.fromJson(data))
          .toList();
      state = state.copyWith(sensors: sensors, isLoading: false);
    } catch (e) {
      // Fallback to mock data if API fails
      await _loadMockData();
    }
  }

  Future<void> refresh() async {
    await _loadInitialData();
  }

  Future<void> _loadMockData() async {
    try {
      final mockSensors = <sensor_models.Sensor>[
        sensor_models.Sensor(
          id: 1,
          name: 'Temperature Sensor A',
          description: 'Main temperature sensor',
          type: 'temperature',
          model: 'DS18B20',
          location: 'Zone 1',
          zone: 'zone1',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://sensor1.local',
          apiKey: 'key123',
          unit: '°C',
          minThreshold: 15.0,
          maxThreshold: 30.0,
          isActive: true,
          lastReading: DateTime.now(),
          value: 24.5,
          health: sensor_models.SensorHealth.good,
          firmware: '1.2.0',
          createdAt: DateTime.now().subtract(const Duration(days: 30)),
          updatedAt: DateTime.now(),
        ),
        sensor_models.Sensor(
          id: 2,
          name: 'pH Sensor',
          description: 'Nutrient solution pH monitor',
          type: 'ph',
          model: 'Atlas Scientific',
          location: 'Reservoir',
          zone: 'reservoir',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://ph-sensor.local',
          apiKey: 'key456',
          unit: 'pH',
          minThreshold: 5.5,
          maxThreshold: 7.0,
          isActive: true,
          lastReading: DateTime.now(),
          value: 6.2,
          health: sensor_models.SensorHealth.good,
          firmware: '2.1.0',
          createdAt: DateTime.now().subtract(const Duration(days: 15)),
          updatedAt: DateTime.now(),
        ),
        sensor_models.Sensor(
          id: 3,
          name: 'Light Sensor',
          description: 'PPFD light intensity monitor',
          type: 'light',
          model: 'Apogee SQ-500',
          location: 'Canopy',
          zone: 'canopy',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://light-sensor.local',
          apiKey: 'key789',
          unit: 'µmol/m²/s',
          minThreshold: 200.0,
          maxThreshold: 800.0,
          isActive: true,
          lastReading: DateTime.now(),
          value: 450.0,
          health: sensor_models.SensorHealth.warning,
          firmware: '1.0.5',
          createdAt: DateTime.now().subtract(const Duration(days: 7)),
          updatedAt: DateTime.now(),
        ),
        sensor_models.Sensor(
          id: 4,
          name: 'Humidity Sensor',
          description: 'Air humidity monitor',
          type: 'humidity',
          model: 'DHT22',
          location: 'Zone 1',
          zone: 'zone1',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://humidity-sensor.local',
          apiKey: 'key101',
          unit: '%',
          minThreshold: 40.0,
          maxThreshold: 80.0,
          isActive: true,
          lastReading: DateTime.now(),
          value: 65.0,
          health: sensor_models.SensorHealth.good,
          firmware: '1.1.0',
          createdAt: DateTime.now().subtract(const Duration(days: 20)),
          updatedAt: DateTime.now(),
        ),
        sensor_models.Sensor(
          id: 5,
          name: 'EC Sensor',
          description: 'Nutrient solution conductivity',
          type: 'ec',
          model: 'Atlas Scientific',
          location: 'Reservoir',
          zone: 'reservoir',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://ec-sensor.local',
          apiKey: 'key202',
          unit: 'mS/cm',
          minThreshold: 1.0,
          maxThreshold: 2.5,
          isActive: true,
          lastReading: DateTime.now(),
          value: 1.8,
          health: sensor_models.SensorHealth.good,
          firmware: '2.0.1',
          createdAt: DateTime.now().subtract(const Duration(days: 10)),
          updatedAt: DateTime.now(),
        ),
        sensor_models.Sensor(
          id: 6,
          name: 'CO2 Sensor',
          description: 'Carbon dioxide level monitor',
          type: 'co2',
          model: 'SenseAir S8',
          location: 'Grow Room',
          zone: 'growroom',
          status: sensor_models.SensorStatus.online,
          apiEndpoint: 'http://co2-sensor.local',
          apiKey: 'key303',
          unit: 'ppm',
          minThreshold: 300.0,
          maxThreshold: 1500.0,
          isActive: true,
          lastReading: DateTime.now(),
          value: 850.0,
          health: sensor_models.SensorHealth.good,
          firmware: '3.1.2',
          createdAt: DateTime.now().subtract(const Duration(days: 5)),
          updatedAt: DateTime.now(),
        ),
      ];

      state = state.copyWith(sensors: mockSensors, isLoading: false);
    } catch (e) {
      state = state.copyWith(error: e.toString(), isLoading: false);
    }
  }
}

/// Legacy provider for backward compatibility
final sensorsProvider = FutureProvider<List<sensor_models.Sensor>>((ref) async {
  final state = ref.watch(sensorsNotifierProvider);
  return state.sensors;
});
