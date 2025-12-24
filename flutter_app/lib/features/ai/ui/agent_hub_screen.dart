import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:cultivar_app/features/admin/widgets/admin_scaffold.dart';
import '../services/agent_api_client.dart';
import '../../../core/theme/app_colors.dart';

/// Agent Hub Screen - Dashboard for all CultivAR AI Agents
/// Uses swarm pattern for parallel agent execution and testing
class AgentHubScreen extends ConsumerStatefulWidget {
  const AgentHubScreen({super.key});

  @override
  ConsumerState<AgentHubScreen> createState() => _AgentHubScreenState();
}

class _AgentHubScreenState extends ConsumerState<AgentHubScreen> {
  List<Map<String, dynamic>> _agents = [];
  Map<String, Map<String, dynamic>> _results = {};
  bool _isLoading = false;
  bool _isTesting = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadAgents();
    });
  }

  Future<void> _loadAgents() async {
    setState(() => _isLoading = true);
    try {
      final agents = await ref.read(agentApiClientProvider).getAgents();
      if (mounted) {
        setState(() {
          _agents = agents;
        });
      }
    } catch (e) {
      if (mounted) _showError(e.toString());
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  Future<void> _testAllAgents() async {
    setState(() {
      _isTesting = true;
      _results = {};
    });

    try {
      final data = await ref.read(agentApiClientProvider).testAllAgents();
      final results = data['results'] as List;

      if (mounted) {
        setState(() {
          for (var result in results) {
            _results[result['agent_id']] = result;
          }
        });
        _showSuccess(
          'Tested ${data['total_agents']} agents: '
          '${data['successful']} passed, ${data['failed']} failed',
        );
      }
    } catch (e) {
      if (mounted) _showError(e.toString());
    } finally {
      if (mounted) setState(() => _isTesting = false);
    }
  }

  Future<void> _executeAgent(
    String agentId,
    String action,
    Map<String, dynamic> params,
  ) async {
    try {
      final result = await ref
          .read(agentApiClientProvider)
          .executeAgent(agentId, action, params);
      if (mounted) {
        setState(() {
          _results[agentId] = result;
        });
      }
    } catch (e) {
      if (mounted) _showError(e.toString());
    }
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: Colors.red),
    );
  }

  void _showSuccess(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message), backgroundColor: AppColors.primary500),
    );
  }

  Map<String, List<Map<String, dynamic>>> get _groupedAgents {
    final groups = <String, List<Map<String, dynamic>>>{
      'discovery': [],
      'growing': [],
      'community': [],
    };

    for (var agent in _agents) {
      final role = agent['role'] as String? ?? 'other';
      if (groups.containsKey(role)) {
        groups[role]!.add(agent);
      } else {
        if (!groups.containsKey('other')) groups['other'] = [];
        groups['other']!.add(agent);
      }
    }
    // Remove empty groups
    groups.removeWhere((key, value) => value.isEmpty);
    return groups;
  }

  String? _getAgentDashboardRoute(String agentId) {
    switch (agentId) {
      case 'plant_health_vision':
        return '/ai/health';
      case 'vpd_optimizer':
        return '/ai/insights';
      case 'grow_buddy':
        return '/ai/guidance';
      case 'nutrient_advisor':
        return '/nutrients/calculator';
      case 'yield_estimator':
        return '/ai/yield';
      // Add more mappings as screens are built
      default:
        return null; // No dedicated dashboard yet
    }
  }

  @override
  Widget build(BuildContext context) {
    return AdminScaffold(
      title: '🤖 Agent Hub',
      actions: [
        IconButton(
          icon: const Icon(Icons.refresh),
          onPressed: _loadAgents,
          tooltip: 'Reload Agents',
        ),
      ],
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _isTesting ? null : _testAllAgents,
        backgroundColor: AppColors.primary500,
        icon: _isTesting
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  color: Colors.white,
                  strokeWidth: 2,
                ),
              )
            : const Icon(Icons.rocket_launch),
        label: Text(_isTesting ? 'Running Swarm...' : 'Test All Models'),
      ),
      body: Container(
        color: AppColors.backgroundDark,
        child: _isLoading
            ? const Center(child: CircularProgressIndicator())
            : CustomScrollView(
                slivers: [
                  SliverToBoxAdapter(child: _buildStatsHeader()),
                  for (final entry in _groupedAgents.entries) ...[
                    SliverPadding(
                      padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
                      sliver: SliverToBoxAdapter(
                        child: _buildSectionHeader(entry.key),
                      ),
                    ),
                    SliverPadding(
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      sliver: SliverGrid(
                        gridDelegate:
                            const SliverGridDelegateWithMaxCrossAxisExtent(
                              maxCrossAxisExtent: 400,
                              mainAxisSpacing: 16,
                              crossAxisSpacing: 16,
                              childAspectRatio: 1.3,
                            ),
                        delegate: SliverChildBuilderDelegate(
                          (context, index) =>
                              _buildAgentCard(entry.value[index]),
                          childCount: entry.value.length,
                        ),
                      ),
                    ),
                  ],
                  const SliverPadding(padding: EdgeInsets.only(bottom: 80)),
                ],
              ),
      ),
    );
  }

  Widget _buildStatsHeader() {
    final passed = _results.values.where((r) => r['success'] == true).length;
    final failed = _results.values.where((r) => r['success'] == false).length;
    final total = _agents.length;
    final pending = total - passed - failed;

    return Container(
      color: AppColors.adminSurface,
      padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 24),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'System Overview',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  '${_agents.length} active agents connected via Swarm Protocol',
                  style: TextStyle(color: Colors.grey[400], fontSize: 13),
                ),
              ],
            ),
          ),
          _buildStatPill('PASSED', passed, AppColors.adminSuccess),
          const SizedBox(width: 8),
          _buildStatPill('FAILED', failed, AppColors.adminDanger),
          const SizedBox(width: 8),
          _buildStatPill('READY', pending, Colors.grey),
        ],
      ),
    );
  }

  Widget _buildStatPill(String label, int value, Color color) {
    if (value == 0 && label != 'READY') return const SizedBox.shrink();
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color.withOpacity(0.5)),
      ),
      child: Row(
        children: [
          Text(
            value.toString(),
            style: TextStyle(
              color: color,
              fontWeight: FontWeight.bold,
              fontSize: 14,
            ),
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 11,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Row(
      children: [
        Icon(
          _getCategoryIcon(title),
          color: _getCategoryColor(title),
          size: 24,
        ),
        const SizedBox(width: 12),
        Text(
          title.toUpperCase(),
          style: const TextStyle(
            color: Colors.white,
            fontSize: 16,
            fontWeight: FontWeight.bold,
            letterSpacing: 1.2,
          ),
        ),
        const SizedBox(width: 8),
        Expanded(child: Divider(color: Colors.grey[800], thickness: 1)),
      ],
    );
  }

  Widget _buildAgentCard(Map<String, dynamic> agent) {
    final agentId = agent['id'] as String;
    final result = _results[agentId];
    final hasResult = result != null;
    final success = result?['success'] ?? false;
    final tools = agent['tools'] as List? ?? [];
    final dashboardRoute = _getAgentDashboardRoute(agentId);

    return Card(
      elevation: 4,
      color: AppColors.adminCard,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: hasResult
            ? BorderSide(
                color: success ? AppColors.adminSuccess : AppColors.adminDanger,
                width: 2,
              )
            : BorderSide.none,
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(10),
                  decoration: BoxDecoration(
                    color: _getCategoryColor(agent['role']).withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Icon(
                    _getCategoryIcon(agent['role']),
                    color: _getCategoryColor(agent['role']),
                    size: 24,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        agent['name'],
                        style: const TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                      Text(
                        agent['role'].toString().toUpperCase(),
                        style: TextStyle(color: Colors.grey[500], fontSize: 10),
                      ),
                    ],
                  ),
                ),
                if (hasResult)
                  Icon(
                    success ? Icons.check_circle : Icons.warning,
                    color: success
                        ? AppColors.adminSuccess
                        : AppColors.adminDanger,
                  ),
              ],
            ),
            const SizedBox(height: 12),
            Expanded(
              child: Text(
                agent['description'] ?? 'No description available.',
                style: TextStyle(
                  color: Colors.grey[400],
                  fontSize: 12,
                  height: 1.4,
                ),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Icon(
                  Icons.build_circle_outlined,
                  size: 14,
                  color: Colors.grey[600],
                ),
                const SizedBox(width: 4),
                Text(
                  '${tools.length} Capabilities',
                  style: TextStyle(color: Colors.grey[600], fontSize: 11),
                ),
                const Spacer(),
                if (hasResult)
                  Text(
                    '${(result['execution_time_ms'] ?? 0).toStringAsFixed(0)}ms',
                    style: TextStyle(color: Colors.grey[600], fontSize: 11),
                  ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton(
                    onPressed: dashboardRoute != null
                        ? () =>
                              context.pushNamed(
                                dashboardRoute.replaceFirst('/', ''),
                              ) // context.goNamed expects name, but we have paths. need name or use push
                        // Actually, let's use the path
                        : null,
                    style: OutlinedButton.styleFrom(
                      side: BorderSide(
                        color: dashboardRoute != null
                            ? AppColors.primary500
                            : Colors.transparent,
                      ),
                      padding: const EdgeInsets.symmetric(vertical: 12),
                    ),
                    child: Text(
                      dashboardRoute != null ? 'Dashboard' : 'Coming Soon',
                      style: TextStyle(
                        color: dashboardRoute != null
                            ? AppColors.primary500
                            : Colors.grey[700],
                      ),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                IconButton.filled(
                  icon: const Icon(Icons.play_arrow_rounded),
                  onPressed: () => _executeAgent(agentId, 'default', {}),
                  tooltip: 'Quick Test',
                  style: IconButton.styleFrom(
                    backgroundColor: Colors.grey[800],
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Color _getCategoryColor(String category) {
    switch (category) {
      case 'discovery':
        return Colors.purpleAccent;
      case 'growing':
        return AppColors.primary500;
      case 'community':
        return Colors.blueAccent;
      default:
        return Colors.grey;
    }
  }

  IconData _getCategoryIcon(String role) {
    switch (role) {
      case 'discovery':
        return Icons.search;
      case 'growing':
        return Icons.local_florist; // eco -> local_florist
      case 'community':
        return Icons.people;
      default:
        return Icons.smart_toy;
    }
  }
}
