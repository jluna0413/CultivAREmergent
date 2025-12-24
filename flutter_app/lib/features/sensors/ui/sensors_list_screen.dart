import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/services/acinfinity_api_service.dart';
import '../../../core/providers/api_client_provider.dart';

/// Provider for AC Infinity API service
final acInfinityServiceProvider = Provider<ACInfinityApiService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return ACInfinityApiService(apiClient);
});

/// Provider for AC Infinity devices list
final acInfinityDevicesProvider = FutureProvider<List<Map<String, dynamic>>>((
  ref,
) async {
  final service = ref.watch(acInfinityServiceProvider);
  return await service.getDevices();
});

class SensorsListScreen extends ConsumerWidget {
  const SensorsListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final devicesAsync = ref.watch(acInfinityDevicesProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('AC Infinity Devices'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => ref.invalidate(acInfinityDevicesProvider),
            tooltip: 'Refresh devices',
          ),
        ],
      ),
      body: devicesAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 16),
              Text(
                'Error loading devices',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              Text(
                error.toString(),
                style: Theme.of(context).textTheme.bodyMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: () => ref.invalidate(acInfinityDevicesProvider),
                icon: const Icon(Icons.refresh),
                label: const Text('Retry'),
              ),
            ],
          ),
        ),
        data: (devices) {
          if (devices.isEmpty) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.device_hub, size: 64, color: Colors.grey[400]),
                  const SizedBox(height: 16),
                  Text(
                    'No AC Infinity devices found',
                    style: Theme.of(context).textTheme.titleLarge,
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Register your first device to get started',
                    style: Theme.of(
                      context,
                    ).textTheme.bodyMedium?.copyWith(color: Colors.grey[600]),
                  ),
                ],
              ),
            );
          }

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: devices.length,
            itemBuilder: (context, index) {
              final device = devices[index];
              return _DeviceCard(device: device);
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {
          // TODO: Navigate to device registration screen
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text('Device registration coming soon!')),
          );
        },
        icon: const Icon(Icons.add),
        label: const Text('Add Device'),
      ),
    );
  }
}

class _DeviceCard extends StatelessWidget {
  const _DeviceCard({required this.device});

  final Map<String, dynamic> device;

  @override
  Widget build(BuildContext context) {
    final deviceId = device['device_id'] as String? ?? 'Unknown';
    final name = device['name'] as String? ?? 'Unnamed Device';
    final type = device['type'] as String? ?? 'Unknown';
    final status = device['status'] as String? ?? 'inactive';
    final isBlocked = device['is_blocked'] as bool? ?? false;
    final securityLevel =
        device['connection_security_level'] as String? ?? 'basic';
    final violations = device['security_violations'] as int? ?? 0;

    final isActive = status == 'active';
    final statusColor = isBlocked
        ? Colors.red
        : isActive
        ? Colors.green
        : Colors.grey;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        contentPadding: const EdgeInsets.all(16),
        leading: Container(
          width: 48,
          height: 48,
          decoration: BoxDecoration(
            color: statusColor.withOpacity(0.1),
            borderRadius: BorderRadius.circular(8),
          ),
          child: Icon(_getDeviceIcon(type), color: statusColor, size: 28),
        ),
        title: Text(
          name,
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            Text('ID: $deviceId'),
            const SizedBox(height: 2),
            Row(
              children: [
                _StatusChip(label: status.toUpperCase(), color: statusColor),
                const SizedBox(width: 8),
                _StatusChip(label: type.toUpperCase(), color: Colors.blue),
              ],
            ),
            if (violations > 0) ...[
              const SizedBox(height: 4),
              Text(
                'Security violations: $violations',
                style: TextStyle(color: Colors.orange[700], fontSize: 12),
              ),
            ],
          ],
        ),
        trailing: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              _getSecurityIcon(securityLevel),
              color: _getSecurityColor(securityLevel),
            ),
            const SizedBox(height: 4),
            Text(
              securityLevel,
              style: TextStyle(
                fontSize: 10,
                color: _getSecurityColor(securityLevel),
              ),
            ),
          ],
        ),
        onTap: () {
          // TODO: Navigate to device details
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(SnackBar(content: Text('View details for $name')));
        },
      ),
    );
  }

  IconData _getDeviceIcon(String type) {
    switch (type.toLowerCase()) {
      case 'controller':
        return Icons.settings_remote;
      case 'fan':
        return Icons.toys;
      case 'sensor':
        return Icons.sensors;
      default:
        return Icons.device_hub;
    }
  }

  IconData _getSecurityIcon(String level) {
    switch (level.toLowerCase()) {
      case 'high':
      case 'secure':
        return Icons.shield;
      case 'basic':
        return Icons.security;
      default:
        return Icons.security_update_warning;
    }
  }

  Color _getSecurityColor(String level) {
    switch (level.toLowerCase()) {
      case 'high':
      case 'secure':
        return Colors.green;
      case 'basic':
        return Colors.orange;
      default:
        return Colors.red;
    }
  }
}

class _StatusChip extends StatelessWidget {
  const _StatusChip({required this.label, required this.color});

  final String label;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(4),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
