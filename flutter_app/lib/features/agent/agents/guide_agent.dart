import 'dart:convert';
import 'package:flutter/foundation.dart';
import '../services/agent_service.dart';

class GuideAgent {
  final AgentService _service;
  final List<Map<String, dynamic>> _messages = [];

  GuideAgent(this._service);

  // System prompt defining the Guide's persona and capabilities
  static const String _systemPrompt = """
You are the CultivAR Guide, a helpful localized assistant for the CultivAR app.
Your goal is to help users navigate the app and answer basic growing questions.

You have access to the following Client-Side Tools:
- navigate_to(route): Go to a specific screen. valid routes: ['/home', '/dashboard', '/marketplace', '/genetics', '/settings', '/camera']
- ask_expert(domain, query): Delegate complex tasks to a server-side expert. domains: ['vision', 'marketplace', 'genetics']

Rules:
1. If the user asks to go somewhere, call `navigate_to`.
2. If the user has a complex question (e.g. "What's wrong with my plant?", "Find a strain with x"), call `ask_expert`.
3. For simple questions ("What is VPD?"), answer directly.
4. Always be concise and friendly.
5. IF you use a tool, output ONLY the tool call strictly in this format: `call:tool_name{args}`.
""";

  /// Initialize the chat with the system prompt
  void init() {
    _messages.clear();
    _messages.add({'role': 'system', 'content': _systemPrompt});
  }

  /// Process a user message and return the agent's response (or action)
  Stream<String> processUserMessage(String userMessage) async* {
    // Add user message to history
    _messages.add({'role': 'user', 'content': userMessage});

    // Construct prompt from history (simplified for basic models)
    // For a real chat model, we'd format this properly as chat template
    final prompt = _buildPrompt();

    try {
      final response = await _service.generate(prompt: prompt);

      // Check for tool calls
      if (response.contains("call:")) {
        yield* _handleToolCall(response);
      } else {
        // Normal text response
        _messages.add({'role': 'assistant', 'content': response});
        yield response;
      }
    } catch (e) {
      yield "Sorry, I'm having trouble thinking right now. ($e)";
    }
  }

  String _buildPrompt() {
    // Simple concatenation for now.
    // Ideally, use the model's specific chat template (e.g. <start_of_turn>...)
    final buffer = StringBuffer();
    for (var msg in _messages) {
      if (msg['role'] == 'system') {
        buffer.writeln("System: ${msg['content']}\n");
      } else if (msg['role'] == 'user') {
        buffer.writeln("User: ${msg['content']}");
      } else {
        buffer.writeln("Guide: ${msg['content']}");
      }
    }
    buffer.writeln("Guide:");
    return buffer.toString();
  }

  Stream<String> _handleToolCall(String response) async* {
    // Parse tool call: call:navigate_to{route:"/marketplace"}
    // Very basic parsing for demo
    final start = response.indexOf("call:");
    final end = response.indexOf("}", start);

    if (start != -1 && end != -1) {
      final toolStr = response.substring(
        start + 5,
        end + 1,
      ); // navigate_to{...}
      final nameEnd = toolStr.indexOf("{");
      final name = toolStr.substring(0, nameEnd).trim();
      final argsStr = toolStr.substring(nameEnd);

      // Notify UI of action
      yield "[Executing $name...]";

      // In a real app, we'd execute the function here.
      // For now, we'll just simulate the action response
      if (name == 'navigate_to') {
        // Extract route (naive parsing)
        final route = argsStr.replaceAll(RegExp(r'[{}"]'), '').split(':')[1];
        yield "CALL_NAVIGATE:$route"; // Signal UI to navigate
      } else if (name == 'ask_expert') {
        yield "CALL_EXPERT:$argsStr"; // Signal UI to call complex API
      }

      _messages.add({'role': 'assistant', 'content': response});
    }
  }
}
