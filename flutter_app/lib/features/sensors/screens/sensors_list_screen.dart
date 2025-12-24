import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:intl/intl.dart';
import 'dart:async';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../../../core/models/sensor_models.dart';
import '../../../core/providers/sensors_provider.dart';
import '../../../core/widgets/loading_indicator.dart';
import '../../../core/widgets/error_view.dart';
import '../../../core/api/websocket_client.dart';

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Create)

enum TimeRange { hour, day, week, month }

class SensorsListScreen extends ConsumerStatefulWidget {
  const SensorsListScreen({super.key});

  @override
  ConsumerState<SensorsListScreen> createState() => _SensorsListScreenState();
}

class _SensorsListScreenState extends ConsumerState<SensorsListScreen>
    with TickerProviderStateMixin {
  late TabController _tabController;
  TimeRange _selectedTimeRange = TimeRange.day;
  Timer? _refreshTimer;
  bool _isWebSocketConnected = false;
  StreamSubscription<Map<String, dynamic>>? _wsSubscription;
  StreamSubscription<WebSocketStatus>? _wsStatusSubscription;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(
      length: 6,
      vsync: this,
    ); // Temperature, Humidity, pH, EC, Light, CO2
    _startAutoRefresh();
    _initWebSocket();
  }

  @override
  void dispose() {
    _tabController.dispose();
    _refreshTimer?.cancel();
    _wsSubscription?.cancel();
    _wsStatusSubscription?.cancel();
    super.dispose();
  }

  void _initWebSocket() {
    final wsClient = WebSocketClient();

    // Listen to WebSocket status changes
    _wsStatusSubscription = wsClient.status.listen((status) {
      if (mounted) {
        setState(() {
          _isWebSocketConnected = status == WebSocketStatus.connected;
        });
      }
    });

    // Listen to sensor data messages
    _wsSubscription = wsClient.messages.listen((message) {
      if (message['type'] == 'sensor_update' && mounted) {
        // Invalidate sensors provider to refresh data
        ref.invalidate(sensorsProvider);
      }
    });

    // Connect to WebSocket
    wsClient.connect();
  }

  void _startAutoRefresh() {
    _refreshTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      if (mounted) {
        ref.invalidate(sensorsProvider);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final sensorsAsync = ref.watch(sensorsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sensor Monitoring Dashboard'),
        backgroundColor: Theme.of(context).primaryColor,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            icon: Icon(
              _isWebSocketConnected ? Icons.wifi : Icons.wifi_off,
              color: _isWebSocketConnected ? Colors.green : Colors.red,
            ),
            onPressed: () {
              // WebSocket connection status
            },
          ),
          PopupMenuButton<TimeRange>(
            onSelected: (TimeRange range) {
              setState(() {
                _selectedTimeRange = range;
              });
            },
            itemBuilder: (BuildContext context) => <PopupMenuEntry<TimeRange>>[
              const PopupMenuItem<TimeRange>(
                value: TimeRange.hour,
                child: Text('Last Hour'),
              ),
              const PopupMenuItem<TimeRange>(
                value: TimeRange.day,
                child: Text('Last Day'),
              ),
              const PopupMenuItem<TimeRange>(
                value: TimeRange.week,
                child: Text('Last Week'),
              ),
              const PopupMenuItem<TimeRange>(
                value: TimeRange.month,
                child: Text('Last Month'),
              ),
            ],
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Text(_getTimeRangeText(_selectedTimeRange)),
                  const Icon(Icons.arrow_drop_down),
                ],
              ),
            ),
          ),
          IconButton(
            icon: const Icon(Icons.download),
            onPressed: () => _exportSensorData(context),
            tooltip: 'Export Sensor Data',
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          tabs: const [
            Tab(text: 'Temperature'),
            Tab(text: 'Humidity'),
            Tab(text: 'pH'),
            Tab(text: 'EC'),
            Tab(text: 'Light'),
            Tab(text: 'CO2'),
          ],
        ),
      ),
      body: sensorsAsync.when(
        data: (sensors) => _buildDashboard(sensors),
        loading: () => const LoadingIndicator(),
        error: (error, stack) => ErrorView(
          message: error.toString(),
          onRetry: () => ref.invalidate(sensorsProvider),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => ref.invalidate(sensorsProvider),
        child: const Icon(Icons.refresh),
      ),
    );
  }

  Widget _buildDashboard(List<Sensor> sensors) {
    if (sensors.isEmpty) {
      return const Center(child: Text('No sensors available'));
    }

    return TabBarView(
      controller: _tabController,
      children: [
        _buildSensorTab(sensors, 'temperature'),
        _buildSensorTab(sensors, 'humidity'),
        _buildSensorTab(sensors, 'ph'),
        _buildSensorTab(sensors, 'ec'),
        _buildSensorTab(sensors, 'light'),
        _buildSensorTab(sensors, 'co2'),
      ],
    );
  }

  Widget _buildSensorTab(List<Sensor> sensors, String sensorType) {
    final filteredSensors = sensors
        .where(
          (sensor) =>
              sensor.type.toLowerCase().contains(sensorType) ||
              sensor.name.toLowerCase().contains(sensorType),
        )
        .toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildSensorGrid(filteredSensors),
          const SizedBox(height: 24),
          _buildChartSection(filteredSensors, sensorType),
          const SizedBox(height: 24),
          _buildAlertsSection(filteredSensors),
        ],
      ),
    );
  }

  Widget _buildSensorGrid(List<Sensor> sensors) {
    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 1.2,
      ),
      itemCount: sensors.length,
      itemBuilder: (context, index) {
        return _buildSensorCard(sensors[index]);
      },
    );
  }

  Widget _buildSensorCard(Sensor sensor) {
    final isOnline = sensor.status == SensorStatus.online;
    final hasAlert = _hasAlert(sensor);

    return Card(
      elevation: 4,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: hasAlert ? Colors.red : Colors.transparent,
          width: 2,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(
                  _getSensorIcon(sensor.type),
                  color: isOnline ? Colors.green : Colors.red,
                  size: 24,
                ),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    sensor.name,
                    style: const TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 16,
                    ),
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              '${sensor.value?.toStringAsFixed(1) ?? 'N/A'} ${sensor.unit ?? ''}',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: _getValueColor(sensor),
              ),
            ),
            const SizedBox(height: 4),
            Text(
              'Status: ${_getStatusText(sensor.status)}',
              style: TextStyle(
                color: isOnline ? Colors.green : Colors.red,
                fontSize: 12,
              ),
            ),
            if (sensor.lastReading != null)
              Text(
                'Last: ${DateFormat('HH:mm').format(sensor.lastReading!)}',
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildChartSection(List<Sensor> sensors, String sensorType) {
    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '${sensorType.toUpperCase()} Trends',
              style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 300,
              child: LineChart(_buildChartData(sensors, sensorType)),
            ),
          ],
        ),
      ),
    );
  }

  LineChartData _buildChartData(List<Sensor> sensors, String sensorType) {
    // Generate sample data for demonstration
    final spots = List.generate(24, (index) {
      final hour = DateTime.now().subtract(Duration(hours: 23 - index));
      double value = 0;

      // Generate realistic sample data based on sensor type
      switch (sensorType) {
        case 'temperature':
          value =
              20 +
              (5 * (index % 3 - 1)) +
              (DateTime.now().millisecondsSinceEpoch % 5);
          break;
        case 'humidity':
          value =
              60 +
              (10 * (index % 3 - 1)) +
              (DateTime.now().millisecondsSinceEpoch % 10);
          break;
        case 'ph':
          value =
              6.5 +
              (0.5 * (index % 3 - 1)) +
              ((DateTime.now().millisecondsSinceEpoch % 10) / 20);
          break;
        case 'ec':
          value =
              1.5 +
              (0.3 * (index % 3 - 1)) +
              ((DateTime.now().millisecondsSinceEpoch % 10) / 30);
          break;
        case 'light':
          value =
              50000 +
              (10000 * (index % 3 - 1)) +
              (DateTime.now().millisecondsSinceEpoch % 1000);
          break;
        case 'co2':
          value =
              800 +
              (100 * (index % 3 - 1)) +
              (DateTime.now().millisecondsSinceEpoch % 50);
          break;
      }

      return FlSpot(hour.hour.toDouble(), value);
    });

    return LineChartData(
      gridData: const FlGridData(show: true),
      titlesData: FlTitlesData(
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            getTitlesWidget: (value, meta) {
              return Text('${value.toInt()}:00');
            },
          ),
        ),
        leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: true)),
        topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
      ),
      borderData: FlBorderData(show: true),
      lineBarsData: [
        LineChartBarData(
          spots: spots,
          isCurved: true,
          color: Theme.of(context).primaryColor,
          barWidth: 3,
          belowBarData: BarAreaData(
            show: true,
            color: Theme.of(context).primaryColor.withValues(alpha: 0.1),
          ),
        ),
      ],
    );
  }

  Widget _buildAlertsSection(List<Sensor> sensors) {
    final alerts = sensors.where(_hasAlert).toList();

    if (alerts.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Row(
            children: [
              Icon(Icons.check_circle, color: Colors.green),
              SizedBox(width: 8),
              Text('All sensors within normal range'),
            ],
          ),
        ),
      );
    }

    return Card(
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.warning, color: Colors.red),
                SizedBox(width: 8),
                Text(
                  'Alerts',
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                    color: Colors.red,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            ...alerts.map((sensor) => _buildAlertItem(sensor)),
          ],
        ),
      ),
    );
  }

  Widget _buildAlertItem(Sensor sensor) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 8),
      child: Row(
        children: [
          Icon(_getSensorIcon(sensor.type), size: 20),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              '${sensor.name}: Value ${sensor.value} ${sensor.unit} is out of range',
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );
  }

  bool _hasAlert(Sensor sensor) {
    if (sensor.value == null ||
        sensor.minThreshold == null ||
        sensor.maxThreshold == null) {
      return false;
    }
    return sensor.value! < sensor.minThreshold! ||
        sensor.value! > sensor.maxThreshold!;
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

  Color _getValueColor(Sensor sensor) {
    if (_hasAlert(sensor)) {
      return Colors.red;
    }
    return Colors.green;
  }

  String _getStatusText(SensorStatus status) {
    switch (status) {
      case SensorStatus.online:
        return 'Online';
      case SensorStatus.offline:
        return 'Offline';
      case SensorStatus.calibrating:
        return 'Calibrating';
      case SensorStatus.error:
        return 'Error';
      case SensorStatus.maintenance:
        return 'Maintenance';
    }
  }

  String _getTimeRangeText(TimeRange range) {
    switch (range) {
      case TimeRange.hour:
        return '1H';
      case TimeRange.day:
        return '1D';
      case TimeRange.week:
        return '1W';
      case TimeRange.month:
        return '1M';
    }
  }

  Future<void> _exportSensorData(BuildContext context) async {
    final scaffoldMessenger = ScaffoldMessenger.of(context);
    try {
      final sensorsAsync = ref.read(sensorsProvider);

      return sensorsAsync.when(
        data: (sensors) async {
          if (sensors.isEmpty) {
            scaffoldMessenger.showSnackBar(
              const SnackBar(content: Text('No sensor data to export')),
            );
            return;
          }

          // Generate CSV content
          final csvHeader =
              'Sensor ID,Name,Type,Model,Location,Zone,Status,Value,Unit,Last Reading,Health\n';
          final csvRows = sensors
              .map((sensor) {
                return '${sensor.id},"${sensor.name}","${sensor.type}","${sensor.model}","${sensor.location ?? ''}","${sensor.zone ?? ''}","${_getStatusText(sensor.status)}","${sensor.value ?? ''}","${sensor.unit ?? ''}","${sensor.lastReading?.toIso8601String() ?? ''}","${_getHealthText(sensor.health)}"';
              })
              .join('\n');

          final csvContent = csvHeader + csvRows;

          // Get temporary directory
          final directory = await getTemporaryDirectory();
          final fileName =
              'sensor_data_${DateFormat('yyyyMMdd_HHmmss').format(DateTime.now())}.csv';
          final file = File('${directory.path}/$fileName');

          // Write CSV content
          await file.writeAsString(csvContent);

          // Share the file - TODO: Update to new SharePlus API
          // await Share.shareXFiles(
          //   [XFile(file.path)],
          //   text: 'Sensor monitoring data export',
          // );

          scaffoldMessenger.showSnackBar(
            SnackBar(content: Text('Data exported to $fileName')),
          );
        },
        loading: () {
          scaffoldMessenger.showSnackBar(
            const SnackBar(content: Text('Loading sensor data...')),
          );
        },
        error: (error, stack) {
          scaffoldMessenger.showSnackBar(
            SnackBar(content: Text('Export failed: ${error.toString()}')),
          );
        },
      );
    } catch (e) {
      scaffoldMessenger.showSnackBar(
        SnackBar(content: Text('Export failed: ${e.toString()}')),
      );
    }
  }

  String _getHealthText(SensorHealth health) {
    switch (health) {
      case SensorHealth.good:
        return 'Good';
      case SensorHealth.warning:
        return 'Warning';
      case SensorHealth.alert:
        return 'Alert';
      case SensorHealth.lowBattery:
        return 'Low Battery';
      case SensorHealth.offline:
        return 'Offline';
    }
  }
}
