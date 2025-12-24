import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:form_builder_validators/form_builder_validators.dart';
import '../../../core/models/sensor_models.dart' as sensor_models;
import '../../../core/models/sensor_models.dart'
    show SensorStatus, SensorHealth;
import '../../../core/providers/sensors_provider.dart';
import '../../../core/widgets/loading_indicator.dart';
import '../../../core/widgets/error_view.dart';
import '../../../core/theme/app_colors.dart';

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Create)

class SensorConfigScreen extends ConsumerStatefulWidget {
  final int sensorId;

  const SensorConfigScreen({super.key, required this.sensorId});

  @override
  ConsumerState<SensorConfigScreen> createState() => _SensorConfigScreenState();
}

// typedef Sensor = sensor_models.Sensor;

class _SensorConfigScreenState extends ConsumerState<SensorConfigScreen> {
  final _formKey = GlobalKey<FormBuilderState>();
  bool _isCalibrating = false;

  @override
  Widget build(BuildContext context) {
    final sensorsAsync = ref.watch(sensorsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sensor Configuration'),
        backgroundColor: AppColors.primary500,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: const Icon(Icons.save),
            onPressed: _saveConfiguration,
          ),
        ],
      ),
      body: sensorsAsync.when(
        data: (sensors) {
          final sensor = sensors.firstWhere(
            (s) => s.id == widget.sensorId,
            orElse: () => sensor_models.Sensor(
              id: 0,
              name: 'Unknown',
              description: null,
              type: 'unknown',
              model: 'unknown',
              location: null,
              zone: null,
              status: SensorStatus.offline,
              apiEndpoint: null,
              apiKey: null,
              unit: null,
              minThreshold: null,
              maxThreshold: null,
              isActive: true,
              lastReading: null,
              value: null,
              health: SensorHealth.good,
              firmware: '1.0.0',
              createdAt: DateTime.now(),
              updatedAt: DateTime.now(),
            ),
          );

          if (sensor.id == 0) {
            return const Center(child: Text('Sensor not found'));
          }

          return _buildConfigForm(sensor);
        },
        loading: () => const LoadingIndicator(),
        error: (error, stack) => ErrorView(
          message: error.toString(),
          onRetry: () => ref.invalidate(sensorsProvider),
        ),
      ),
    );
  }

  Widget _buildConfigForm(sensor_models.Sensor sensor) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: FormBuilder(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSensorInfo(sensor),
            const SizedBox(height: 24),
            _buildBasicSettings(sensor),
            const SizedBox(height: 24),
            _buildThresholdsSection(sensor),
            const SizedBox(height: 24),
            _buildCalibrationSection(sensor),
            const SizedBox(height: 24),
            _buildAdvancedSettings(sensor),
          ],
        ),
      ),
    );
  }

  Widget _buildSensorInfo(sensor_models.Sensor sensor) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  _getSensorIcon(sensor.type),
                  size: 32,
                  color: AppColors.primary500,
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        sensor.name,
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        '${sensor.type} - ${sensor.model}',
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ],
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 6,
                  ),
                  decoration: BoxDecoration(
                    color: sensor.status == SensorStatus.online
                        ? Colors.green
                        : Colors.red,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    sensor.status.toString().split('.').last.toUpperCase(),
                    style: const TextStyle(color: Colors.white, fontSize: 12),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: _buildInfoItem(
                    'Current Value',
                    '${sensor.value ?? 'N/A'} ${sensor.unit ?? ''}',
                  ),
                ),
                Expanded(
                  child: _buildInfoItem(
                    'Location',
                    sensor.location ?? 'Not set',
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: _buildInfoItem(
                    'Last Reading',
                    sensor.lastReading != null
                        ? '${sensor.lastReading!.hour}:${sensor.lastReading!.minute.toString().padLeft(2, '0')}'
                        : 'Never',
                  ),
                ),
                Expanded(child: _buildInfoItem('Firmware', sensor.firmware)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildInfoItem(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 12)),
        Text(value, style: const TextStyle(fontWeight: FontWeight.w500)),
      ],
    );
  }

  Widget _buildBasicSettings(sensor_models.Sensor sensor) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Basic Settings',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'name',
              initialValue: sensor.name,
              decoration: const InputDecoration(
                labelText: 'Sensor Name',
                border: OutlineInputBorder(),
              ),
              validator: FormBuilderValidators.required(),
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'location',
              initialValue: sensor.location,
              decoration: const InputDecoration(
                labelText: 'Location',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'zone',
              initialValue: sensor.zone,
              decoration: const InputDecoration(
                labelText: 'Zone',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            FormBuilderSwitch(
              name: 'isActive',
              title: const Text('Active'),
              initialValue: sensor.isActive,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildThresholdsSection(sensor_models.Sensor sensor) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Thresholds & Alerts',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: FormBuilderTextField(
                    name: 'minThreshold',
                    initialValue: sensor.minThreshold?.toString(),
                    decoration: const InputDecoration(
                      labelText: 'Min Threshold',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                    validator: FormBuilderValidators.numeric(),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: FormBuilderTextField(
                    name: 'maxThreshold',
                    initialValue: sensor.maxThreshold?.toString(),
                    decoration: const InputDecoration(
                      labelText: 'Max Threshold',
                      border: OutlineInputBorder(),
                    ),
                    keyboardType: TextInputType.number,
                    validator: FormBuilderValidators.numeric(),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            FormBuilderDropdown<String>(
              name: 'health',
              initialValue: sensor.health.toString().split('.').last,
              decoration: const InputDecoration(
                labelText: 'Health Status',
                border: OutlineInputBorder(),
              ),
              items: SensorHealth.values
                  .map(
                    (health) => DropdownMenuItem(
                      value: health.toString().split('.').last,
                      child: Text(health.toString().split('.').last),
                    ),
                  )
                  .toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildCalibrationSection(sensor_models.Sensor sensor) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Calibration',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            if (_isCalibrating)
              const Column(
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Calibrating sensor...'),
                ],
              )
            else
              Column(
                children: [
                  const Text(
                    'Calibrate the sensor to ensure accurate readings. Place the sensor in a known environment and click calibrate.',
                    style: TextStyle(color: Colors.grey),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      Expanded(
                        child: ElevatedButton.icon(
                          onPressed: () => _startCalibration(sensor),
                          icon: const Icon(Icons.tune),
                          label: const Text('Start Calibration'),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.primary500,
                            foregroundColor: Colors.white,
                          ),
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: OutlinedButton.icon(
                          onPressed: () => _resetCalibration(sensor),
                          icon: const Icon(Icons.restore),
                          label: const Text('Reset'),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildAdvancedSettings(sensor_models.Sensor sensor) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Advanced Settings',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'apiEndpoint',
              initialValue: sensor.apiEndpoint,
              decoration: const InputDecoration(
                labelText: 'API Endpoint',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'apiKey',
              initialValue: sensor.apiKey,
              decoration: const InputDecoration(
                labelText: 'API Key',
                border: OutlineInputBorder(),
              ),
              obscureText: true,
            ),
            const SizedBox(height: 16),
            FormBuilderTextField(
              name: 'unit',
              initialValue: sensor.unit,
              decoration: const InputDecoration(
                labelText: 'Unit',
                border: OutlineInputBorder(),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void _saveConfiguration() {
    if (_formKey.currentState?.saveAndValidate() ?? false) {
      final formData = _formKey.currentState!.value;
      // TODO: Implement save logic with API call
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Configuration saved successfully')),
      );
    }
  }

  void _startCalibration(sensor_models.Sensor sensor) {
    setState(() {
      _isCalibrating = true;
    });

    // Simulate calibration process
    Future.delayed(const Duration(seconds: 3), () {
      if (mounted) {
        setState(() {
          _isCalibrating = false;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Calibration completed successfully')),
        );
      }
    });
  }

  void _resetCalibration(sensor_models.Sensor sensor) {
    // TODO: Implement reset calibration logic
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Calibration reset')));
  }

  IconData _getSensorIcon(String type) {
    final lowerType = type.toLowerCase();
    if (lowerType.contains('temperature') || lowerType.contains('temp')) {
      return Icons.thermostat;
    } else if (lowerType.contains('humidity')) {
      return Icons.water_drop;
    } else if (lowerType.contains('ph')) {
      return Icons.science;
    } else if (lowerType.contains('ec') || lowerType.contains('conductivity')) {
      return Icons.flash_on;
    } else if (lowerType.contains('light')) {
      return Icons.wb_sunny;
    } else if (lowerType.contains('co2')) {
      return Icons.air;
    }
    return Icons.sensors;
  }
}
