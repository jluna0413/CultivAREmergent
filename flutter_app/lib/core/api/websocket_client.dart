// lib/core/api/websocket_client.dart
import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import '../../core/constants/app_constants.dart';

enum WebSocketStatus {
  connecting,
  connected,
  reconnecting,
  disconnected,
  error,
}

class WebSocketClient {
  factory WebSocketClient() {
    return _singleton;
  }

  WebSocketClient._internal();
  static final WebSocketClient _singleton = WebSocketClient._internal();
  WebSocketChannel? _channel;
  final FlutterSecureStorage _secureStorage = const FlutterSecureStorage();
  Timer? _reconnectTimer;
  Timer? _pingTimer;
  int _reconnectAttempts = 0;
  final Duration _pingInterval = const Duration(seconds: 30);

  final StreamController<Map<String, dynamic>> _messageController =
      StreamController<Map<String, dynamic>>.broadcast();
  Stream<Map<String, dynamic>> get messages => _messageController.stream;

  final StreamController<WebSocketStatus> _statusController =
      StreamController<WebSocketStatus>.broadcast();
  Stream<WebSocketStatus> get status => _statusController.stream;

  Future<void> connect() async {
    _statusController.add(WebSocketStatus.connecting);
    _reconnectTimer?.cancel(); // Cancel any existing reconnect timer

    try {
      final accessToken = await _secureStorage.read(
        key: AppConstants.accessTokenKey,
      );
      if (accessToken == null) {
        _statusController.add(WebSocketStatus.error);
        _messageController.add({
          'type': 'error',
          'message': 'No access token found for WebSocket.',
        });
        return;
      }

      final uri = Uri.parse('${AppConstants.wsBaseUrl}?token=$accessToken');
      _channel = WebSocketChannel.connect(uri);

      _channel!.stream.listen(
        (message) {
          if (kDebugMode) {
            print('WebSocket message received: $message');
          }
          if (message is! String) {
            _messageController.add({
              'type': 'error',
              'message': 'Invalid message type',
            });
            return;
          }
          try {
            final data = jsonDecode(message) as Map<String, dynamic>;
            _messageController.add(data);
          } catch (e) {
            if (kDebugMode) {
              print('Failed to decode WebSocket message: $e');
            }
            _messageController.add({
              'type': 'error',
              'message': 'Invalid message format.',
            });
          }
        },
        onDone: () {
          if (kDebugMode) {
            print('WebSocket disconnected.');
          }
          _statusController.add(WebSocketStatus.disconnected);
          _scheduleReconnect();
        },
        onError: (error) {
          if (kDebugMode) {
            print('WebSocket error: $error');
          }
          _statusController.add(WebSocketStatus.error);
          _scheduleReconnect();
        },
        cancelOnError: true,
      );

      _statusController.add(WebSocketStatus.connected);
      _reconnectAttempts =
          0; // Reset reconnect attempts on successful connection
      _startPing();
      if (kDebugMode) {
        print('WebSocket connected to $uri');
      }
    } catch (e) {
      if (kDebugMode) {
        print('WebSocket connection failed: $e');
      }
      _statusController.add(WebSocketStatus.error);
      _scheduleReconnect();
    }
  }

  void _startPing() {
    _pingTimer?.cancel();
    _pingTimer = Timer.periodic(_pingInterval, (timer) {
      if (_channel != null) {
        try {
          _channel!.sink.add('ping'); // Send a ping message
        } catch (e) {
          if (kDebugMode) {
            print('Failed to send WebSocket ping: $e');
          }
          _pingTimer?.cancel();
          _scheduleReconnect();
        }
      }
    });
  }

  void _scheduleReconnect() {
    _reconnectTimer?.cancel();
    if (_reconnectAttempts < 5) {
      // Limit reconnect attempts
      _reconnectAttempts++;
      final delay = Duration(
        seconds: _reconnectAttempts * 2,
      ); // Exponential backoff
      if (kDebugMode) {
        print('Attempting to reconnect WebSocket in $delay...');
      }
      _statusController.add(WebSocketStatus.reconnecting);
      _reconnectTimer = Timer(delay, () => connect());
    } else {
      if (kDebugMode) {
        print(
          'Max WebSocket reconnect attempts reached. Staying disconnected.',
        );
      }
      _statusController.add(WebSocketStatus.disconnected);
    }
  }

  void disconnect() {
    if (_channel != null) {
      _channel!.sink.close();
      _channel = null;
    }
    _reconnectTimer?.cancel();
    _pingTimer?.cancel();
    _statusController.add(WebSocketStatus.disconnected);
    if (kDebugMode) {
      print('WebSocket explicitly disconnected.');
    }
  }

  void sendMessage(String message) {
    if (_channel != null) {
      _channel!.sink.add(message);
    } else {
      if (kDebugMode) {
        print('WebSocket not connected. Message not sent: $message');
      }
    }
  }

  // Example subscription method (can be generalized)
  Stream<Map<String, dynamic>> subscribe(String topic) {
    // For now, we'll just filter the main message stream.
    // In a more complex setup, you might send a 'subscribe' message to the server.
    return messages.where((event) => event['topic'] == topic);
  }

  void dispose() {
    disconnect();
    _messageController.close();
    _statusController.close();
  }
}
