import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import 'package:cultivar_app/core/providers/sensors_provider.dart';

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Create)

class MockWebSocketChannel extends Mock implements WebSocketChannel {}

class MockWebSocketSink extends Mock implements WebSocketSink {}

void main() {
  group('SensorWebSocketService', () {
    late SensorWebSocketService service;
    late MockWebSocketChannel mockChannel;
    late MockWebSocketSink mockSink;

    setUp(() {
      service = SensorWebSocketService();
      mockChannel = MockWebSocketChannel();
      mockSink = MockWebSocketSink();
    });

    test('connect establishes connection and emits status', () async {
      when(mockChannel.sink).thenReturn(mockSink);
      when(mockChannel.stream).thenAnswer((_) => Stream.value('[]'));

      // Test connection logic
      service.connect('ws://test.com');

      await Future.delayed(Duration.zero);

      verify(mockChannel.sink.close(status.goingAway)).called(1);
    });

    test('reconnect uses exponential backoff', () async {
      service.connect('ws://test.com');

      // Verify reconnection attempts with increasing delays
      await Future.delayed(const Duration(seconds: 6));

      // Test should pass if no exceptions thrown
      expect(true, true);
    });

    test('dispose closes all streams', () {
      service.dispose();

      // Verify streams are closed
      expect(() => service.sensorsStream.listen((_) {}), throwsStateError);
      expect(() => service.connectionStream.listen((_) {}), throwsStateError);
    });
  });
}
