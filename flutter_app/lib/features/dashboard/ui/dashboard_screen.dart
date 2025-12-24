import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:intl/intl.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/providers/dashboard_provider.dart';
import '../../../../core/widgets/stat_card.dart';
import '../../../../core/theme/app_navigation_drawer.dart';
// import '../../plants/domain/plant_model.dart'; // Unused
import '../../../../core/widgets/plant_card.dart';
import '../../../../core/state/auth_provider.dart';

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Scaffold(
      backgroundColor: const Color(0xFF1a1a1a),
      appBar: AppBar(
        backgroundColor: const Color(0xFF2a2a2a),
        title: const Text('Dashboard', style: TextStyle(color: Colors.white)),
        iconTheme: const IconThemeData(color: Colors.white),
        actions: [
          Consumer(
            builder: (context, ref, child) {
              final isLoading = ref.watch(dashboardLoadingProvider);
              return IconButton(
                icon: Icon(isLoading ? Icons.hourglass_empty : Icons.refresh),
                onPressed: isLoading
                    ? null
                    : () {
                        // Invalidate and refetch dashboard stats
                        ref.invalidate(dashboardStatsProvider);
                      },
              );
            },
          ),
          // Logout button
          IconButton(
            icon: const Icon(Icons.logout, color: Colors.redAccent),
            tooltip: 'Logout',
            onPressed: () async {
              await ref.read(authProvider.notifier).logout();
              if (context.mounted) {
                context.go('/login');
              }
            },
          ),
          IconButton(
            icon: const Icon(Icons.more_vert),
            onPressed: () {
              // TODO: Show dropdown menu with export options
            },
          ),
        ],
      ),
      drawer: const AppNavigationDrawer(),
      body: const SingleChildScrollView(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Quick Stats Row
            _QuickStatsSection(),

            SizedBox(height: 24),

            // Main Content Row
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Plants Overview (Left Column - 8/12 width)
                Expanded(flex: 8, child: _PlantsOverviewSection()),

                SizedBox(width: 24),

                // Environmental Data & Recent Activity (Right Column - 4/12 width)
                Expanded(
                  flex: 4,
                  child: Column(
                    children: [
                      _EnvironmentalDataSection(),
                      SizedBox(height: 24),
                      _RecentActivitySection(),
                    ],
                  ),
                ),
              ],
            ),

            SizedBox(height: 24),

            // Quick Actions
            _QuickActionsSection(),
          ],
        ),
      ),
    );
  }
}

class _QuickStatsSection extends ConsumerWidget {
  const _QuickStatsSection();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final totalPlants = ref.watch(totalPlantsProvider);
    final activePlants = ref.watch(activePlantsProvider);
    final strains = ref.watch(strainsProvider);
    final harvestedPlants = ref.watch(harvestedPlantsProvider);
    final isLoading = ref.watch(dashboardLoadingProvider);
    final error = ref.watch(dashboardErrorProvider);

    // Show loading state
    if (isLoading) {
      return const Row(
        children: [
          Expanded(
            child: StatCard(
              label: 'Total Plants',
              value: '...',
              icon: Icons.local_florist,
              color: Colors.green,
            ),
          ),
          SizedBox(width: 16),
          Expanded(
            child: StatCard(
              label: 'Active Plants',
              value: '...',
              icon: Icons.grass,
              color: Colors.blue,
            ),
          ),
          SizedBox(width: 16),
          Expanded(
            child: StatCard(
              label: 'Strains',
              value: '...',
              icon: Icons.science,
              color: Colors.purple,
            ),
          ),
          SizedBox(width: 16),
          Expanded(
            child: StatCard(
              label: 'Harvested',
              value: '...',
              icon: Icons.cut,
              color: Colors.orange,
            ),
          ),
        ],
      );
    }

    // Show error state
    if (error != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            children: [
              Icon(
                Icons.error_outline,
                size: 48,
                color: Colors.red.withOpacity(0.7),
              ),
              const SizedBox(height: 8),
              Text(
                'Failed to load dashboard stats',
                style: TextStyle(color: Colors.red.withOpacity(0.7)),
              ),
              const SizedBox(height: 4),
              Text(
                error,
                style: TextStyle(
                  color: Colors.white.withOpacity(0.6),
                  fontSize: 12,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      );
    }

    // Show data
    return Row(
      children: [
        Expanded(
          child: StatCard(
            label: 'Total Plants',
            value: totalPlants.toString(),
            icon: Icons.local_florist,
            color: Colors.green,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: StatCard(
            label: 'Active Plants',
            value: activePlants.toString(),
            icon: Icons.grass,
            color: Colors.blue,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: StatCard(
            label: 'Strains',
            value: strains.toString(),
            icon: Icons.science,
            color: Colors.purple,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: StatCard(
            label: 'Harvested',
            value: harvestedPlants.toString(),
            icon: Icons.cut,
            color: Colors.orange,
          ),
        ),
      ],
    );
  }
}

class _PlantsOverviewSection extends ConsumerWidget {
  const _PlantsOverviewSection();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final recentPlantsAsync = ref.watch(recentPlantsProvider);
    // ); // Removed this line

    return Card(
      color: const Color(0xFF2a2a2a),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text(
                  'My Plants',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                PopupMenuButton<String>(
                  onSelected: (value) {
                    switch (value) {
                      case 'view_all':
                        context.go('/plants');
                        break;
                      case 'add_new':
                        context.go('/plants/new');
                        break;
                    }
                  },
                  itemBuilder: (context) => [
                    const PopupMenuItem(
                      value: 'view_all',
                      child: Text('View All Plants'),
                    ),
                    const PopupMenuItem(
                      value: 'add_new',
                      child: Text('Add New Plant'),
                    ),
                  ],
                  child: const Icon(Icons.more_vert, color: Colors.white70),
                ),
              ],
            ),
            const SizedBox(height: 16),
            recentPlantsAsync.when(
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => Center(
                child: Column(
                  children: [
                    Icon(
                      Icons.error_outline,
                      size: 48,
                      color: Colors.red.withOpacity(0.7),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      'Failed to load plants',
                      style: TextStyle(color: Colors.red.withOpacity(0.7)),
                    ),
                  ],
                ),
              ),
              data: (plants) {
                if (plants.isEmpty) {
                  return const _EmptyPlantsState();
                } else {
                  return ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: plants.length,
                    itemBuilder: (context, index) {
                      final plant = plants[index];
                      // Assuming PlantCard exists and takes a Plant object
                      return PlantCard(
                        name: plant.name,
                        strain: plant.strainName ?? 'Unknown',
                        imageUrl: plant.imageUrl,
                        status: PlantStatus(
                          label: plant.statusName ?? 'Active',
                          color: Colors.green, // Default or map from statusId
                        ),
                        onTap: () => context.go('/plants/${plant.id}'),
                      );
                    },
                  );
                }
              },
            ),
          ],
        ),
      ),
    );
  }
}

class _EmptyPlantsState extends StatelessWidget {
  const _EmptyPlantsState();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(40.0),
        child: Column(
          children: [
            Icon(
              Icons.local_florist,
              size: 64,
              color: Colors.white.withOpacity(0.3),
            ),
            const SizedBox(height: 16),
            const Text(
              'No plants yet',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            const Text(
              'Start your grow journal by adding your first plant.',
              style: TextStyle(color: Colors.white70, fontSize: 16),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => context.go('/plants/new'),
              icon: const Icon(Icons.add),
              label: const Text('Add First Plant'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.green,
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _PlantsTable extends StatelessWidget {
  const _PlantsTable();

  @override
  Widget build(BuildContext context) {
    // TODO: Implement actual plants table
    return const Text(
      'Plants table coming soon...',
      style: TextStyle(color: Colors.white70),
    );
  }
}

class _EnvironmentalDataSection extends ConsumerWidget {
  const _EnvironmentalDataSection();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final dashboardStatsAsync = ref.watch(dashboardStatsProvider);
    // ); // Removed this line

    return dashboardStatsAsync.when(
      loading: () => Card(
        color: const Color(0xFF2a2a2a),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Environmental Data',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              const Center(child: CircularProgressIndicator()),
              const SizedBox(height: 16),
              Center(
                child: Text(
                  'Loading...',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.6),
                    fontSize: 12,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      error: (error, stack) => Card(
        color: const Color(0xFF2a2a2a),
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                'Environmental Data',
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),
              Center(
                child: Icon(
                  Icons.error_outline,
                  size: 48,
                  color: Colors.red.withOpacity(0.7),
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Failed to load environmental data',
                style: TextStyle(color: Colors.red.withOpacity(0.7)),
              ),
            ],
          ),
        ),
      ),
      data: (dashboardStats) {
        final avgTemperature = dashboardStats.environment.avgTemperature;
        final avgHumidity = dashboardStats.environment.avgHumidity;
        final avgPh = dashboardStats.environment.avgPh;
        final avgEc = dashboardStats.environment.avgEc;
        final lastReadingTime = dashboardStats.sensors.lastReadingTime;

        String formattedLastUpdated = lastReadingTime != null
            ? DateFormat('MMM d, hh:mm a').format(lastReadingTime)
            : 'Never';

        return Card(
          color: const Color(0xFF2a2a2a),
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  'Environmental Data',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: _EnvironmentalMetric(
                        value: '${avgTemperature.toStringAsFixed(1)}°F',
                        label: 'Temperature',
                        icon: Icons.thermostat,
                        color: Colors.red,
                      ),
                    ),
                    Expanded(
                      child: _EnvironmentalMetric(
                        value: '${avgHumidity.toStringAsFixed(1)}%',
                        label: 'Humidity',
                        icon: Icons.water_drop,
                        color: Colors.blue,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: _EnvironmentalMetric(
                        value: avgPh != null ? avgPh.toStringAsFixed(1) : '--',
                        label: 'pH',
                        icon: Icons.science, // Changed icon to reflect pH
                        color: Colors.yellow,
                      ),
                    ),
                    Expanded(
                      child: _EnvironmentalMetric(
                        value: avgEc != null
                            ? '${avgEc.toStringAsFixed(1)} EC'
                            : '-- EC',
                        label: 'EC',
                        icon: Icons.grass, // Changed icon to reflect EC
                        color: Colors.green,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                Center(
                  child: Text(
                    'Last updated: $formattedLastUpdated',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.6),
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}

class _EnvironmentalMetric extends StatelessWidget {
  final String value;
  final String label;
  final IconData icon;
  final Color color;

  const _EnvironmentalMetric({
    required this.value,
    required this.label,
    required this.icon,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: TextStyle(
            color: color,
            fontSize: 24,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 12),
        ),
      ],
    );
  }
}

class _RecentActivitySection extends ConsumerWidget {
  const _RecentActivitySection();

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final activitiesAsync = ref.watch(recentActivitiesProvider);

    return Card(
      color: const Color(0xFF2a2a2a),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Recent Activity',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            if (activitiesAsync.isEmpty)
              Center(
                child: Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Column(
                    children: [
                      Icon(
                        Icons.history,
                        size: 48,
                        color: Colors.white.withOpacity(0.3),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'No recent activity',
                        style: TextStyle(color: Colors.white.withOpacity(0.6)),
                      ),
                    ],
                  ),
                ),
              )
            else
              ListView.builder(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: activitiesAsync.length,
                itemBuilder: (context, index) {
                  final activity = activitiesAsync[index];
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 12.0),
                    child: Row(
                      children: [
                        Icon(
                          _getActivityIcon(activity.activityType),
                          size: 20,
                          color: _getActivityColor(activity.severity),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                activity.description,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 14,
                                ),
                              ),
                              const SizedBox(height: 2),
                              Text(
                                _formatTimestamp(activity.timestamp),
                                style: TextStyle(
                                  color: Colors.white.withOpacity(0.6),
                                  fontSize: 12,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  );
                },
              ),
          ],
        ),
      ),
    );
  }

  IconData _getActivityIcon(String activityType) {
    switch (activityType.toLowerCase()) {
      case 'watering':
        return Icons.water_drop;
      case 'feeding':
        return Icons.science;
      case 'harvesting':
        return Icons.cut;
      case 'planting':
        return Icons.spa;
      case 'measurement':
        return Icons.straighten;
      case 'note':
        return Icons.note;
      default:
        return Icons.history;
    }
  }

  Color _getActivityColor(String severity) {
    switch (severity.toLowerCase()) {
      case 'high':
        return Colors.red;
      case 'medium':
        return Colors.orange;
      case 'low':
        return Colors.green;
      default:
        return Colors.blue;
    }
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inDays > 0) {
      return '${difference.inDays}d ago';
    } else if (difference.inHours > 0) {
      return '${difference.inHours}h ago';
    } else if (difference.inMinutes > 0) {
      return '${difference.inMinutes}m ago';
    } else {
      return 'Just now';
    }
  }
}

class _QuickActionsSection extends StatelessWidget {
  const _QuickActionsSection();

  @override
  Widget build(BuildContext context) {
    return Card(
      color: const Color(0xFF2a2a2a),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Quick Actions',
              style: TextStyle(
                color: Colors.white,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _QuickActionButton(
                    icon: Icons.add,
                    label: 'Add Plant',
                    onPressed: () => context.go('/plants/new'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _QuickActionButton(
                    icon: Icons.science,
                    label: 'Add Strain',
                    onPressed: () => context.go('/strains'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _QuickActionButton(
                    icon: Icons.task,
                    label: 'Log Activity',
                    onPressed: () => context.go('/plants/new'),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _QuickActionButton(
                    icon: Icons.calendar_today,
                    label: 'View Calendar',
                    onPressed: () {
                      // TODO: Implement calendar view
                    },
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

class _QuickActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const _QuickActionButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: const Color(0xFF3a3a3a),
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 12),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 20),
          const SizedBox(height: 4),
          Text(
            label,
            style: const TextStyle(fontSize: 12),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
