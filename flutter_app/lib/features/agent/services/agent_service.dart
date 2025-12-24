import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class AgentService {
  // Default to localhost for Android emulator (10.0.2.2) or local device
  // Update this based on where Ollama is running (e.g. PC IP if on phone)
  static const String _baseUrl = 'http://10.0.2.2:11434';
  static const String _model = 'cultivar-function-gemma:latest';

  Future<String> generate({
    required String prompt,
    List<Map<String, dynamic>>? context,
  }) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'model': _model,
          'prompt': prompt,
          'stream': false,
          // 'context': context, // Pass previous context context if managing history
          'options': {'temperature': 0.7, 'top_p': 0.9},
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] as String;
      } else {
        throw Exception('Failed to generate response: ${response.statusCode}');
      }
    } catch (e) {
      debugPrint('AgentService Error: $e');
      // Fallback for demo/dev if Ollama isn't reachable
      return "I'm having trouble connecting to my brain. Please check if Ollama is running.";
    }
  }

  /// Check if the local model is available
  Future<bool> isServiceAvailable() async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/api/tags'));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
