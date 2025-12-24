import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter/foundation.dart';

class ExpertService {
  // Python Backend URL (FastAPI)
  // Use 10.0.2.2 for Android Emulator, localhost for iOS/Web, or your LAN IP
  static const String _baseUrl = 'http://10.0.2.2:4200';

  Future<String> askExpert(String domain, String query) async {
    try {
      final response = await http
          .post(
            Uri.parse('$_baseUrl/agents/query'),
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'domain': domain,
              'query': query,
              'stream': false,
            }),
          )
          .timeout(const Duration(seconds: 30));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        // Assuming backend returns { "response": "..." } or similar
        return data['response'] ??
            data['result'] ??
            "Expert completed the task.";
      } else {
        return "The Expert Agent is currently unavailable (Status: ${response.statusCode}).";
      }
    } catch (e) {
      debugPrint('ExpertService Error: $e');
      return "I couldn't reach the Expert Agent. Please check your connection.";
    }
  }
}
