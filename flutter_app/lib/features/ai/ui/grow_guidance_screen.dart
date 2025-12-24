import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../services/agent_api_client.dart';
import '../../admin/widgets/admin_scaffold.dart';

class GrowGuidanceScreen extends ConsumerStatefulWidget {
  const GrowGuidanceScreen({super.key});

  @override
  ConsumerState<GrowGuidanceScreen> createState() => _GrowGuidanceScreenState();
}

class _GrowGuidanceScreenState extends ConsumerState<GrowGuidanceScreen> {
  final TextEditingController _controller = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final List<ChatMessage> _messages = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    // Add initial welcome message
    _messages.add(
      ChatMessage(
        text:
            "Hi! I'm your Grow Buddy. Ask me about watering, nutrients, lighting, or tell me what issues you're facing!",
        isUser: false,
      ),
    );
  }

  Future<void> _sendMessage(
    String text, {
    String? action,
    String? topic,
  }) async {
    if (text.trim().isEmpty && action == null) return;

    setState(() {
      _messages.add(ChatMessage(text: text, isUser: true));
      _isLoading = true;
    });
    _scrollToBottom();
    _controller.clear();

    try {
      Map<String, dynamic> result;
      String agentAction = 'get_advice';
      Map<String, dynamic> params = {};

      if (action == 'daily_tip') {
        agentAction = 'daily_tip';
        params = {
          'experience_level': 'intermediate',
        }; // TODO: Pull from user profile
      } else {
        // Default to getting advice
        params = {
          'current_issue': text,
          'experience_level': 'intermediate', // TODO: Pull from user profile
        };
        if (topic != null) {
          params['topic'] = topic;
        }
      }

      final response = await ref
          .read(agentApiClientProvider)
          .executeAgent('grow_buddy', agentAction, params);

      final agentResponse = response['result'] as Map<String, dynamic>;
      String responseText = '';

      if (action == 'daily_tip') {
        responseText =
            "🌱 **Daily Tip:**\n${agentResponse['tip']}\n\n_${agentResponse['share']}_";
      } else {
        // Parse advice response
        if (agentResponse['specific_advice'] != null) {
          responseText += "${agentResponse['specific_advice']}\n\n";
        }

        final adviceList = agentResponse['advice'] as List<dynamic>?;
        if (adviceList != null && adviceList.isNotEmpty) {
          responseText += "**Key Tips:**\n";
          for (var tip in adviceList) {
            responseText += "• $tip\n";
          }
        }

        if (agentResponse['pro_tip'] != null) {
          responseText += "\n**💡 Pro Tip:** ${agentResponse['pro_tip']}";
        }
      }

      if (mounted) {
        setState(() {
          _messages.add(ChatMessage(text: responseText, isUser: false));
          _isLoading = false;
        });
        _scrollToBottom();
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _messages.add(
            ChatMessage(text: "Error: $e", isUser: false, isError: true),
          );
          _isLoading = false;
        });
        _scrollToBottom();
      }
    }
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return AdminScaffold(
      title: '🌱 Grow Guidance',
      body: Column(
        children: [
          // Quick Actions
          Container(
            padding: const EdgeInsets.all(12),
            color: AppColors.adminCard,
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _QuickActionChip(
                    label: 'Daily Tip',
                    icon: Icons.lightbulb_outline,
                    onTap: () => _sendMessage(
                      'Give me a daily tip',
                      action: 'daily_tip',
                    ),
                  ),
                  _QuickActionChip(
                    label: 'Watering',
                    icon: Icons.water_drop_outlined,
                    onTap: () =>
                        _sendMessage('Watering advice', topic: 'watering'),
                  ),
                  _QuickActionChip(
                    label: 'Nutrients',
                    icon: Icons.science_outlined,
                    onTap: () =>
                        _sendMessage('Nutrient advice', topic: 'nutrients'),
                  ),
                  _QuickActionChip(
                    label: 'Lighting',
                    icon: Icons.wb_sunny_outlined,
                    onTap: () =>
                        _sendMessage('Lighting advice', topic: 'lighting'),
                  ),
                ],
              ),
            ),
          ),

          // Chat Area
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final msg = _messages[index];
                return _ChatBubble(message: msg);
              },
            ),
          ),

          // Input Area
          Container(
            padding: const EdgeInsets.all(16),
            color: AppColors.adminCard,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: 'Ask about your grow...',
                      hintStyle: TextStyle(color: Colors.grey[500]),
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                        borderSide: BorderSide.none,
                      ),
                      filled: true,
                      fillColor: Colors.black26,
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 20,
                        vertical: 12,
                      ),
                    ),
                    onSubmitted: (val) => _sendMessage(val),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton(
                  onPressed: _isLoading
                      ? null
                      : () => _sendMessage(_controller.text),
                  icon: _isLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            color: AppColors.primary500,
                          ),
                        )
                      : const Icon(Icons.send, color: AppColors.primary500),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ChatMessage {
  final String text;
  final bool isUser;
  final bool isError;

  ChatMessage({required this.text, required this.isUser, this.isError = false});
}

class _ChatBubble extends StatelessWidget {
  final ChatMessage message;

  const _ChatBubble({required this.message});

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        constraints: BoxConstraints(
          maxWidth: MediaQuery.of(context).size.width * 0.75,
        ),
        decoration: BoxDecoration(
          color: isUser
              ? AppColors.primary500
              : (message.isError
                    ? AppColors.danger.withOpacity(0.2)
                    : Colors.grey[800]),
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
        ),
        child: Text(
          message.text,
          style: const TextStyle(color: Colors.white, height: 1.4),
        ),
      ),
    );
  }
}

class _QuickActionChip extends StatelessWidget {
  final String label;
  final IconData icon;
  final VoidCallback onTap;

  const _QuickActionChip({
    required this.label,
    required this.icon,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(right: 8),
      child: ActionChip(
        avatar: Icon(icon, size: 16, color: AppColors.primary500),
        label: Text(label, style: const TextStyle(color: Colors.white)),
        backgroundColor: Colors.black26,
        onPressed: onTap,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        side: BorderSide.none,
      ),
    );
  }
}
