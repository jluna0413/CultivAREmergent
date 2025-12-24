import 'package:flutter/material.dart';
import 'package:cultivar_app/features/admin/widgets/admin_scaffold.dart';
import 'package:go_router/go_router.dart';
import 'package:cultivar_app/core/theme/app_colors.dart';

class AdminDashboardScreen extends StatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  String _currentTime = '';
  bool _isLoadingActivities = false;
  List<String> _recentLogs = [];

  @override
  void initState() {
    super.initState();
    _updateCurrentTime();
    _loadRecentLogs();

    // Update time every second
    Future.doWhile(() async {
      await Future.delayed(const Duration(seconds: 1));
      if (mounted) {
        _updateCurrentTime();
        return true;
      }
      return false;
    });
  }

  void _updateCurrentTime() {
    final now = DateTime.now();
    setState(() {
      _currentTime = now.toString();
    });
  }

  void _loadRecentLogs() {
    // Simulate loading recent logs
    setState(() {
      _recentLogs = [
        '[2023-05-01 12:34:56] INFO: Application started',
        '[2023-05-01 12:35:01] INFO: User login successful',
        '[2023-05-01 12:36:12] ERROR: Database connection failed',
        '[2023-05-01 12:36:15] INFO: Database connection restored',
        '[2023-05-01 12:40:22] INFO: Plant added: Blue Dream',
        '[2023-05-01 12:45:33] INFO: Sensor reading: Temp=78.5°F, Humidity=65%',
        '[2023-05-01 13:01:45] WARN: High temperature detected: 85.2°F',
      ];
    });
  }

  @override
  Widget build(BuildContext context) {
    return AdminScaffold(
      title: 'Dashboard',
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Statistics Cards Row
          Row(
            children: [
              Expanded(
                child: _buildStatCard(
                  title: 'Total Plants',
                  value: '156',
                  icon: Icons.local_florist,
                  color: AppColors.adminPrimary,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  title: 'Active Strains',
                  value: '42',
                  icon: Icons.science,
                  color: AppColors.adminSuccess,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  title: 'Sensors',
                  value: '23',
                  icon: Icons.thermostat,
                  color: AppColors.adminInfo,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  title: 'Users',
                  value: '8',
                  icon: Icons.people,
                  color: AppColors.adminWarning,
                ),
              ),
            ],
          ),

          const SizedBox(height: 24),

          // Agent Ecosystem Section
          _buildAgentEcosystemCard(),

          const SizedBox(height: 24),

          // Content Rows
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // System Information Column
              Expanded(
                flex: 2,
                child: Column(
                  children: [
                    _buildSystemInfoCard(),
                    const SizedBox(height: 16),
                    _buildDiagnosticsCard(),
                  ],
                ),
              ),

              const SizedBox(width: 16),

              // Activities and Logs Column
              Expanded(
                flex: 2,
                child: Column(
                  children: [
                    _buildRecentActivitiesCard(),
                    const SizedBox(height: 16),
                    _buildRecentLogsCard(),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAgentEcosystemCard() {
    return _buildCard(
      title: 'Agent Ecosystem',
      action: ElevatedButton.icon(
        onPressed: () => context.goNamed('agent-hub'),
        icon: const Icon(Icons.psychology, size: 18),
        label: const Text('Open Hub'),
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.adminPrimary,
          foregroundColor: Colors.white,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.check_circle, color: AppColors.adminSuccess, size: 20),
              SizedBox(width: 8),
              Text(
                'System Status: All Agents Operational',
                style: TextStyle(
                  color: AppColors.textPrimaryDark,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              _buildAgentStat(
                'Discovery',
                '4 Agents',
                Icons.search,
                AppColors.adminInfo,
              ),
              const SizedBox(width: 24),
              _buildAgentStat(
                'Growing',
                '4 Agents',
                Icons.local_florist,
                AppColors.adminSuccess,
              ),
              const SizedBox(width: 24),
              _buildAgentStat(
                'Community',
                '3 Agents',
                Icons.people,
                AppColors.adminWarning,
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAgentStat(
    String label,
    String value,
    IconData icon,
    Color color,
  ) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 12),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              label,
              style: const TextStyle(
                color: AppColors.textSecondaryDark,
                fontSize: 12,
              ),
            ),
            Text(
              value,
              style: const TextStyle(
                color: AppColors.textPrimaryDark,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStatCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.adminCard,
        borderRadius: BorderRadius.circular(8),
        border: Border(left: BorderSide(color: color, width: 4)),
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: color,
                    fontSize: 12,
                    fontWeight: FontWeight.bold,
                    letterSpacing: 0.5,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  value,
                  style: const TextStyle(
                    color: AppColors.textPrimaryDark,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          Icon(icon, size: 32, color: AppColors.textTertiaryDark),
        ],
      ),
    );
  }

  Widget _buildSystemInfoCard() {
    return _buildCard(
      title: 'System Information',
      child: _buildInfoTable({
        'Python Version': '3.9.7',
        'Flask Version': '2.3.2',
        'Database': 'SQLite (15.2 MB)',
        'Operating System': 'Linux 5.4.0',
        'Server Time': _currentTime.isNotEmpty
            ? _currentTime.substring(0, 19)
            : 'Loading...',
        'System Uptime': '2 days, 14 hours',
      }),
    );
  }

  Widget _buildDiagnosticsCard() {
    return _buildCard(
      title: 'JavaScript Diagnostics',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Enable JavaScript diagnostics to debug client-side issues. This will add a diagnostics panel to all pages.',
            style: TextStyle(color: AppColors.textSecondaryDark, fontSize: 14),
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              ElevatedButton(
                onPressed: () {
                  _showSuccessMessage('JavaScript diagnostics enabled');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.adminPrimary,
                  foregroundColor: Colors.white,
                ),
                child: const Text('Enable Diagnostics'),
              ),
              const SizedBox(width: 8),
              ElevatedButton(
                onPressed: () {
                  _showInfoMessage('JavaScript diagnostics disabled');
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.adminDanger,
                  foregroundColor: Colors.white,
                ),
                child: const Text('Disable Diagnostics'),
              ),
            ],
          ),
          const SizedBox(height: 16),
          const Divider(),
          const SizedBox(height: 16),
          const Text(
            'Diagnostics Status',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimaryDark,
            ),
          ),
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.adminInfo.withOpacity(0.1),
              borderRadius: BorderRadius.circular(6),
              border: Border.all(color: AppColors.adminInfo.withOpacity(0.3)),
            ),
            child: const Row(
              children: [
                Icon(Icons.info, color: AppColors.adminInfo, size: 16),
                SizedBox(width: 8),
                Expanded(
                  child: Text(
                    'JavaScript diagnostics are currently disabled.',
                    style: TextStyle(
                      color: AppColors.textSecondaryDark,
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecentActivitiesCard() {
    return _buildCard(
      title: 'Recent Activities',
      action: IconButton(
        onPressed: _refreshActivities,
        icon: const Icon(Icons.refresh, color: AppColors.primary500),
        tooltip: 'Refresh activities',
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Activity',
            style: TextStyle(
              fontWeight: FontWeight.w600,
              color: AppColors.textPrimaryDark,
              fontSize: 12,
            ),
          ),
          const SizedBox(height: 16),
          if (_isLoadingActivities)
            const Center(
              child: CircularProgressIndicator(color: AppColors.primary500),
            )
          else
            Column(
              children: [
                _buildActivityItem(
                  type: 'login',
                  typeText: 'Login',
                  icon: Icons.login,
                  details: 'User login',
                  user: 'admin',
                  time: '2 min ago',
                ),
                const Divider(),
                _buildActivityItem(
                  type: 'plant_add',
                  typeText: 'Plant Added',
                  icon: Icons.local_florist,
                  details: 'Added Blue Dream',
                  user: 'john',
                  time: '5 min ago',
                ),
                const Divider(),
                _buildActivityItem(
                  type: 'sensor_reading',
                  typeText: 'Sensor',
                  icon: Icons.thermostat,
                  details: 'Temp: 78.5°F, Humidity: 65%',
                  user: 'system',
                  time: '10 min ago',
                ),
              ],
            ),
        ],
      ),
    );
  }

  Widget _buildActivityItem({
    required String type,
    required String typeText,
    required IconData icon,
    required String details,
    required String user,
    required String time,
  }) {
    Color badgeColor;
    switch (type) {
      case 'login':
        badgeColor = AppColors.adminInfo;
        break;
      case 'plant_add':
        badgeColor = AppColors.adminSuccess;
        break;
      case 'sensor_reading':
        badgeColor = AppColors.adminPrimary;
        break;
      default:
        badgeColor = AppColors.adminWarning;
    }

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: badgeColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                Icon(icon, size: 12, color: badgeColor),
                const SizedBox(width: 4),
                Text(
                  typeText,
                  style: TextStyle(
                    color: badgeColor,
                    fontSize: 10,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  details,
                  style: const TextStyle(
                    color: AppColors.textPrimaryDark,
                    fontSize: 12,
                  ),
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    Text(
                      user,
                      style: const TextStyle(
                        color: AppColors.textSecondaryDark,
                        fontSize: 10,
                      ),
                    ),
                    const Text(
                      ' • ',
                      style: TextStyle(
                        color: AppColors.textTertiaryDark,
                        fontSize: 10,
                      ),
                    ),
                    Text(
                      time,
                      style: const TextStyle(
                        color: AppColors.textTertiaryDark,
                        fontSize: 10,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildRecentLogsCard() {
    return _buildCard(
      title: 'Recent Logs',
      action: TextButton(
        onPressed: _viewAllLogs,
        child: const Text(
          'View All Logs',
          style: TextStyle(color: AppColors.primary500, fontSize: 12),
        ),
      ),
      child: Container(
        height: 200,
        decoration: BoxDecoration(
          color: Colors.black.withOpacity(0.1),
          borderRadius: BorderRadius.circular(4),
        ),
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: _recentLogs.map((log) {
              final isError = log.contains('ERROR');
              final isWarn = log.contains('WARN');
              Color textColor;

              if (isError) {
                textColor = AppColors.adminDanger;
              } else if (isWarn) {
                textColor = AppColors.adminWarning;
              } else {
                textColor = AppColors.textTertiaryDark;
              }

              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 2),
                child: Text(
                  log,
                  style: TextStyle(
                    color: textColor,
                    fontSize: 10,
                    fontFamily: 'monospace',
                  ),
                ),
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  Widget _buildCard({
    required String title,
    required Widget child,
    Widget? action,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppColors.adminCard,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                title,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimaryDark,
                ),
              ),
              if (action != null) action,
            ],
          ),
          const SizedBox(height: 16),
          child,
        ],
      ),
    );
  }

  Widget _buildInfoTable(Map<String, String> data) {
    return Table(
      columnWidths: const {0: FlexColumnWidth(1), 1: FlexColumnWidth(2)},
      children: data.entries.map((entry) {
        return TableRow(
          children: [
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                entry.key,
                style: const TextStyle(
                  fontWeight: FontWeight.w600,
                  color: AppColors.textPrimaryDark,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(
                entry.value,
                style: const TextStyle(color: AppColors.textSecondaryDark),
              ),
            ),
          ],
        );
      }).toList(),
    );
  }

  void _refreshActivities() {
    setState(() {
      _isLoadingActivities = true;
    });

    Future.delayed(const Duration(seconds: 1), () {
      if (mounted) {
        setState(() {
          _isLoadingActivities = false;
        });
        _showSuccessMessage('Activities refreshed');
      }
    });
  }

  void _viewAllLogs() {
    _showInfoMessage(
      'View all logs functionality would open a detailed logs modal',
    );
  }

  void _showSuccessMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: AppColors.adminSuccess,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  void _showInfoMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: AppColors.adminInfo,
        behavior: SnackBarBehavior.floating,
      ),
    );
  }
}
