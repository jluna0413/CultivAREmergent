import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_riverpod/flutter_riverpod.dart';

class AgentApiClient {
  final String _baseUrl = 'http://localhost:4200/api/v2/agents';

  Future<List<Map<String, dynamic>>> getAgents() async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/list'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return List<Map<String, dynamic>>.from(data['agents'] ?? []);
      } else {
        throw Exception('Failed to load agents: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to agent server: $e');
    }
  }

  Future<Map<String, dynamic>> testAllAgents() async {
    try {
      final response = await http.post(Uri.parse('$_baseUrl/test-all'));
      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('Failed to run swarm test: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to agent server: $e');
    }
  }

  Future<Map<String, dynamic>> testCategory(String category) async {
    try {
      final response = await http.get(Uri.parse('$_baseUrl/test/$category'));
      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception(
          'Failed to test category $category: ${response.statusCode}',
        );
      }
    } catch (e) {
      throw Exception('Failed to connect to agent server: $e');
    }
  }

  Future<Map<String, dynamic>> executeAgent(
    String agentId,
    String action,
    Map<String, dynamic> params,
  ) async {
    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/execute'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'agent_id': agentId,
          'action': action,
          'params': params,
        }),
      );
      if (response.statusCode == 200) {
        return json.decode(response.body) as Map<String, dynamic>;
      } else {
        throw Exception('Failed to execute agent: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Failed to connect to agent server: $e');
    }
  }
}

final agentApiClientProvider = Provider<AgentApiClient>(
  (ref) => AgentApiClient(),
);
