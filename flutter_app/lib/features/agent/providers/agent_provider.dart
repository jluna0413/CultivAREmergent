import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../services/agent_service.dart';
import 'guide_agent.dart';

// Service Provider
final agentServiceProvider = Provider<AgentService>((ref) {
  return AgentService();
});

// Guide Agent Provider
// Using StateNotifier or similar might be better for chat state,
// but for now we expose the logical class.
final guideAgentProvider = Provider<GuideAgent>((ref) {
  final service = ref.watch(agentServiceProvider);
  final agent = GuideAgent(service);
  agent.init();
  return agent;
});

// Chat State Provider (List of messages to display in UI)
class ChatStateNotifier extends StateNotifier<List<Map<String, String>>> {
  final GuideAgent _agent;

  ChatStateNotifier(this._agent) : super([]);

  void addUserMessage(String message) async {
    state = [
      ...state,
      {'role': 'user', 'content': message},
    ];

    // Get stream
    try {
      // Create a temporary placeholder for assistant
      state = [
        ...state,
        {'role': 'assistant', 'content': '...'},
      ];

      String fullResponse = "";
      bool isAction = false;

      await for (final chunk in _agent.processUserMessage(message)) {
        // logic to handle special action signals from agent
        if (chunk.startsWith("CALL_NAVIGATE:")) {
          // This logic should ideally be handled by a side-effect or controller
          // For simple state, we just show the action text
          isAction = true;
          fullResponse = "Navigating to ${chunk.split(':')[1]}...";
        } else if (chunk.startsWith("CALL_EXPERT:")) {
          isAction = true;
          fullResponse = "Connecting you to an Expert...";
        } else {
          fullResponse = chunk;
        }

        // Update the last message (assistant)
        final newState = List<Map<String, String>>.from(state);
        newState.last = {'role': 'assistant', 'content': fullResponse};
        state = newState;
      }
    } catch (e) {
      state = [
        ...state,
        {'role': 'assistant', 'content': 'Error: $e'},
      ];
    }
  }
}

final chatStateProvider =
    StateNotifierProvider<ChatStateNotifier, List<Map<String, String>>>((ref) {
      final agent = ref.watch(guideAgentProvider);
      return ChatStateNotifier(agent);
    });
