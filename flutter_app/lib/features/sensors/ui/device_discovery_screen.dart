import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/providers/sensors_provider.dart';

/// Device Discovery and Management Screen for AC Infinity devices
class DeviceDiscoveryScreen extends ConsumerStatefulWidget {
  const DeviceDiscoveryScreen({super.key});

  @override
  ConsumerState<DeviceDiscoveryScreen> createState() =>
      _DeviceDiscoveryScreenState();
}

class _DeviceDiscoveryScreenState extends ConsumerState<DeviceDiscoveryScreen> {
  bool _isScanning = false;
  String? _scanError;
  List<Map<String, dynamic>> _discoveredDevices = [];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final sensorsState = ref.watch(sensorsNotifierProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Device Management'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
      ),
      body: Column(
        children: [
          _buildScanSection(theme),
          Expanded(child: _buildDeviceList(sensorsState, theme)),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _isScanning ? null : _scanForDevices,
        backgroundColor: _isScanning ? Colors.grey : const Color(0xFF4CAF50),
        icon: _isScanning
            ? const SizedBox(
                width: 20,
                height: 20,
                child: CircularProgressIndicator(
                  strokeWidth: 2,
                  valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                ),
              )
            : const Icon(Icons.search),
        label: Text(_isScanning ? 'Scanning...' : 'Scan for Devices'),
      ),
    );
  }

  Widget _buildScanSection(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.all(16),
      color: theme.primaryColor.withOpacity(0.1),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'AC Infinity Device Discovery',
            style: theme.textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Scan your network for AC Infinity controllers and sensors. Make sure your devices are powered on and connected to the same network.',
            style: theme.textTheme.bodyMedium,
          ),
          if (_scanError != null) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.red.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(color: Colors.red.withOpacity(0.3)),
              ),
              child: Row(
                children: [
                  const Icon(Icons.error_outline, color: Colors.red),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      _scanError!,
                      style: const TextStyle(color: Colors.red),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildDeviceList(SensorsState sensorsState, ThemeData theme) {
    if (sensorsState.isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    final registeredDevices = sensorsState.sensors
        .where(
          (sensor) => sensor.source == 'acinfinity' && sensor.device != null,
        )
        .map((sensor) => sensor.device!)
        .toSet()
        .toList();

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        if (registeredDevices.isNotEmpty) ...[
          _buildSectionHeader('Registered Devices', theme),
          ...registeredDevices.map(
            (deviceId) => _buildRegisteredDeviceCard(deviceId, theme),
          ),
          const SizedBox(height: 24),
        ],

        if (_discoveredDevices.isNotEmpty) ...[
          _buildSectionHeader('Discovered Devices', theme),
          ..._discoveredDevices.map(
            (device) => _buildDiscoveredDeviceCard(device, theme),
          ),
        ] else if (!_isScanning && _scanError == null) ...[
          _buildEmptyState(theme),
        ],
      ],
    );
  }

  Widget _buildSectionHeader(String title, ThemeData theme) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Text(
        title,
        style: theme.textTheme.titleMedium?.copyWith(
          fontWeight: FontWeight.w600,
          color: theme.primaryColor,
        ),
      ),
    );
  }

  Widget _buildRegisteredDeviceCard(String deviceId, ThemeData theme) {
    final deviceSensors = ref
        .watch(sensorsNotifierProvider)
        .sensors
        .where((sensor) => sensor.device == deviceId)
        .toList();

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(
                  Icons.device_hub,
                  color: Color(0xFF4CAF50),
                  size: 24,
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    'AC Infinity Controller',
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.green.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Text(
                    'Connected',
                    style: TextStyle(
                      color: Colors.green,
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Device ID: $deviceId',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.textTheme.bodySmall?.color?.withOpacity(0.7),
              ),
            ),
            const SizedBox(height: 12),
            Text(
              '${deviceSensors.length} sensors connected',
              style: theme.textTheme.bodyMedium,
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => _viewDeviceDetails(deviceId),
                    icon: const Icon(Icons.visibility),
                    label: const Text('View Details'),
                  ),
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: OutlinedButton.icon(
                    onPressed: () => _configureDevice(deviceId),
                    icon: const Icon(Icons.settings),
                    label: const Text('Configure'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDiscoveredDeviceCard(
    Map<String, dynamic> device,
    ThemeData theme,
  ) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.wifi, color: Colors.orange, size: 24),
                const SizedBox(width: 12),
                Expanded(
                  child: Text(
                    device['name'] ?? 'AC Infinity Device',
                    style: theme.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 8,
                    vertical: 4,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.orange.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Text(
                    'Discovered',
                    style: TextStyle(
                      color: Colors.orange,
                      fontSize: 12,
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Device ID: ${device['id']}',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.textTheme.bodySmall?.color?.withOpacity(0.7),
              ),
            ),
            if (device['sensors'] != null) ...[
              const SizedBox(height: 8),
              Text(
                '${device['sensors'].length} sensors available',
                style: theme.textTheme.bodyMedium,
              ),
            ],
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => _registerDevice(device),
                style: ElevatedButton.styleFrom(
                  backgroundColor: const Color(0xFF4CAF50),
                  foregroundColor: Colors.white,
                ),
                icon: const Icon(Icons.add),
                label: const Text('Add to System'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState(ThemeData theme) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.device_unknown, size: 64, color: theme.disabledColor),
          const SizedBox(height: 16),
          Text(
            'No devices found',
            style: theme.textTheme.titleMedium?.copyWith(
              color: theme.disabledColor,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            'Tap the scan button to search for AC Infinity devices on your network',
            style: theme.textTheme.bodyMedium?.copyWith(
              color: theme.disabledColor,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Future<void> _scanForDevices() async {
    setState(() {
      _isScanning = true;
      _scanError = null;
    });

    try {
      // Simulate device discovery for now
      await Future.delayed(const Duration(seconds: 3));

      // Mock discovered devices
      setState(() {
        _discoveredDevices = [
          {
            'id': 'ACINF-001',
            'name': 'AC Infinity Controller Pro',
            'sensors': ['temperature', 'humidity', 'co2'],
          },
          {
            'id': 'ACINF-002',
            'name': 'AC Infinity Cloudport',
            'sensors': ['temperature', 'humidity', 'light'],
          },
        ];
      });
    } catch (e) {
      setState(() {
        _scanError = 'Failed to scan for devices: ${e.toString()}';
      });
    } finally {
      setState(() {
        _isScanning = false;
      });
    }
  }

  void _viewDeviceDetails(String deviceId) {
    // Navigate to device details screen
    context.go('/sensors/device/$deviceId');
  }

  void _configureDevice(String deviceId) {
    // Navigate to device configuration screen
    context.go('/sensors/device/$deviceId/configure');
  }

  Future<void> _registerDevice(Map<String, dynamic> device) async {
    // TODO: Implement device registration
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Device ${device['name']} registered successfully'),
        backgroundColor: Colors.green,
      ),
    );

    // Remove from discovered devices and refresh registered devices
    setState(() {
      _discoveredDevices.removeWhere((d) => d['id'] == device['id']);
    });

    // Refresh sensors list
    ref.read(sensorsNotifierProvider.notifier).refresh();
  }
}
