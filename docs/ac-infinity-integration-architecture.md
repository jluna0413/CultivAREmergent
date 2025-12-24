# AC Infinity Hardware Integration Architecture

## Overview

This document outlines the architecture for completing the AC Infinity hardware integration in CultivAR's MVP. The integration connects existing backend models with the comprehensive frontend UI to enable real-time sensor monitoring from AC Infinity devices.

## Current State Analysis

### ✅ Backend (Complete)
- **Models**: `ACInfinityDevice` and `ACInfinityToken` with security features
- **Handlers**: `scan_ac_infinity_sensors()` function in `sensor_handlers.py`
- **Security**: API key hashing, device fingerprinting, rate limiting

### ⚠️ Frontend (Mock Data Only)
- **Models**: Complete sensor models with health/status tracking
- **UI**: Comprehensive dashboard with charts, real-time updates, alerts
- **Provider**: Advanced Riverpod provider with WebSocket support
- **Issue**: All data is mocked, no backend connection

### ❌ Integration Gap
- No API routes for sensor data
- Frontend API client not connected
- No device management UI
- WebSocket configuration missing

## Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AC Infinity   │    │   CultivAR      │    │   Flutter App   │
│   Hardware      │◄──►│   Backend       │◄──►│   Frontend      │
│   Devices       │    │   API           │    │   UI            │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   Device API              Sensor Routes          Sensor Provider
   (External)              (/api/sensors)         (Riverpod)
```

## Implementation Plan

### Phase 1: Backend API Routes

#### 1.1 Sensor API Routes (`app/routes/sensor_routes.py`)
```python
# New file: app/routes/sensor_routes.py
from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.handlers.sensor_handlers import (
    get_sensors, get_sensor_data, scan_ac_infinity_sensors,
    create_sensor, update_sensor, delete_sensor
)

sensor_bp = Blueprint('sensor', __name__, url_prefix='/api/sensors')

@sensor_bp.route('/', methods=['GET'])
@login_required
def get_sensors_route():
    """Get all sensors for the current user."""
    sensors = get_sensors()
    return jsonify(sensors)

@sensor_bp.route('/<int:sensor_id>', methods=['GET'])
@login_required
def get_sensor_route(sensor_id):
    """Get sensor data and readings."""
    data = get_sensor_data(sensor_id)
    return jsonify(data)

@sensor_bp.route('/scan/ac-infinity', methods=['POST'])
@login_required
def scan_ac_infinity():
    """Scan for AC Infinity devices and sensors."""
    result = scan_ac_infinity_sensors()
    return jsonify(result)

@sensor_bp.route('/', methods=['POST'])
@login_required
def create_sensor_route():
    """Create a new sensor."""
    data = request.get_json()
    # Implementation needed
    return jsonify({"success": False, "error": "Not implemented"})

@sensor_bp.route('/<int:sensor_id>', methods=['PUT'])
@login_required
def update_sensor_route(sensor_id):
    """Update sensor configuration."""
    data = request.get_json()
    # Implementation needed
    return jsonify({"success": False, "error": "Not implemented"})
```

#### 1.2 Register Routes (`app/routes/routes.py`)
```python
# Add to register_routes function
from .sensor_routes import sensor_bp

def register_routes(app):
    # ... existing routes ...
    app.register_blueprint(sensor_bp)
```

### Phase 2: Frontend API Integration

#### 2.1 Update API Client (`flutter_app/lib/core/api/api_client.dart`)
```dart
// Add sensor methods to ApiClient
class ApiClient {
  // ... existing methods ...

  Future<List<Map<String, dynamic>>> getSensors() async {
    final response = await _dio.get('/api/sensors');
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<Map<String, dynamic>> getSensor(int sensorId) async {
    final response = await _dio.get('/api/sensors/$sensorId');
    return response.data;
  }

  Future<Map<String, dynamic>> scanACInfinityDevices() async {
    final response = await _dio.post('/api/sensors/scan/ac-infinity');
    return response.data;
  }

  Future<Map<String, dynamic>> createSensor(Map<String, dynamic> sensorData) async {
    final response = await _dio.post('/api/sensors', data: sensorData);
    return response.data;
  }

  Future<Map<String, dynamic>> updateSensor(int sensorId, Map<String, dynamic> sensorData) async {
    final response = await _dio.put('/api/sensors/$sensorId', data: sensorData);
    return response.data;
  }
}
```

#### 2.2 Update Sensor Provider (`flutter_app/lib/core/providers/sensors_provider.dart`)
```dart
// Replace mock data loading with real API calls
Future<void> _loadInitialData() async {
  state = state.copyWith(isLoading: true);

  try {
    final apiClient = ref.read(apiClientProvider);
    final sensorsData = await apiClient.getSensors();

    final sensors = sensorsData.map((data) => Sensor.fromJson(data)).toList();
    state = state.copyWith(sensors: sensors, isLoading: false);
  } catch (e) {
    state = state.copyWith(error: e.toString(), isLoading: false);
  }
}

// Update WebSocket URL to match backend
_webSocketService?.connect('ws://your-backend-url/ws/sensors');
```

### Phase 3: Device Management UI

#### 3.1 Device Discovery Screen
```dart
// New file: flutter_app/lib/features/sensors/ui/device_discovery_screen.dart
class DeviceDiscoveryScreen extends ConsumerWidget {
  const DeviceDiscoveryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      appBar: AppBar(title: const Text('Device Discovery')),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: () => _scanForDevices(ref),
            child: const Text('Scan for AC Infinity Devices'),
          ),
          // Device list with connection status
        ],
      ),
    );
  }

  Future<void> _scanForDevices(WidgetRef ref) async {
    final apiClient = ref.read(apiClientProvider);
    try {
      final result = await apiClient.scanACInfinityDevices();
      // Handle success/failure
    } catch (e) {
      // Handle error
    }
  }
}
```

### Phase 4: Real-time Data Flow

#### 4.1 Backend WebSocket Implementation
```python
# New file: app/websocket/sensor_ws.py
from flask_socketio import emit, join_room, leave_room
import json

def handle_sensor_connect():
    """Handle WebSocket connection for sensors."""
    join_room('sensors')
    emit('status', {'message': 'Connected to sensor updates'})

def handle_sensor_disconnect():
    """Handle WebSocket disconnection."""
    leave_room('sensors')

def broadcast_sensor_update(sensor_data):
    """Broadcast sensor data to all connected clients."""
    emit('sensor_update', sensor_data, room='sensors')
```

#### 4.2 Frontend WebSocket Integration
```dart
// Update SensorWebSocketService in sensors_provider.dart
void connect(String url) {
  // ... existing connection logic ...
  _channel = WebSocketChannel.connect(Uri.parse(url));

  _channel!.stream.listen(
    (message) {
      final data = jsonDecode(message);
      if (data['type'] == 'sensor_update') {
        // Update sensor data in provider
        _updateSensorData(data['payload']);
      }
    },
    // ... error handling ...
  );
}
```

## Data Flow Architecture

### Sensor Data Pipeline
1. **Device Level**: AC Infinity devices collect sensor data
2. **API Level**: Backend polls devices via AC Infinity API
3. **Database Level**: Sensor readings stored in PostgreSQL
4. **WebSocket Level**: Real-time updates pushed to frontend
5. **UI Level**: Provider updates trigger reactive UI changes

### Security Architecture
- **Device Authentication**: API key hashing and device fingerprinting
- **Token Management**: Secure token storage with expiration
- **Rate Limiting**: Per-device and per-user limits
- **IP Restrictions**: Configurable allowed IP ranges
- **Audit Logging**: All device communications logged

## Testing Strategy

### Unit Tests
- Sensor model validation
- API client request/response handling
- Provider state management
- WebSocket message parsing

### Integration Tests
- End-to-end sensor data flow
- Device discovery and registration
- Real-time update propagation
- Error handling and recovery

### Hardware Tests
- AC Infinity device connectivity
- Sensor data accuracy validation
- Network interruption handling
- Device offline/online transitions

## Deployment Considerations

### Environment Configuration
```yaml
# config/production.yaml
ac_infinity:
  api_url: "https://api.acinfinity.com/v2"
  timeout: 30
  retry_attempts: 3

websocket:
  url: "wss://api.cultivar.app/ws/sensors"
  ping_interval: 30
  reconnect_delay: 5
```

### Monitoring and Observability
- Device connection health checks
- Sensor data quality metrics
- WebSocket connection monitoring
- API rate limit tracking
- Error rate and latency monitoring

## Success Criteria

### Functional Requirements
- ✅ AC Infinity devices auto-discovered and registered
- ✅ Real-time sensor data displayed in dashboard
- ✅ Device connection status monitoring
- ✅ Historical sensor data charting
- ✅ Alert system for sensor thresholds

### Performance Requirements
- ✅ WebSocket latency < 100ms
- ✅ Sensor data refresh < 5 seconds
- ✅ Dashboard load time < 2 seconds
- ✅ Memory usage < 50MB for sensor data

### Security Requirements
- ✅ All device communications encrypted
- ✅ API keys never stored in plain text
- ✅ Rate limiting prevents abuse
- ✅ Audit logs for all device operations

## Next Steps

1. **Immediate**: Implement sensor API routes
2. **Week 1**: Connect frontend API client to backend
3. **Week 2**: Implement device discovery UI
4. **Week 3**: Enable real-time WebSocket updates
5. **Week 4**: Testing, monitoring, and production deployment

This architecture provides a solid foundation for hardware-agnostic sensor integration while prioritizing the AC Infinity MVP requirements.