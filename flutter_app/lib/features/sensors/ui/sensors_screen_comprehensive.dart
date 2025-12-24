import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:math' as math;

import '../../../core/logging.dart';

/// Comprehensive Sensor Monitoring Dashboard
class SensorsScreen extends ConsumerStatefulWidget {
  const SensorsScreen({super.key});

  @override
  ConsumerState<SensorsScreen> createState() => _SensorsScreenState();
}

class _SensorsScreenState extends ConsumerState<SensorsScreen> {
  final PageController _pageController = PageController();
  int _currentPage = 0;
  final List<String> _timeRanges = ['1H', '6H', '24H', '7D'];
  int _selectedTimeRange = 0;
  bool _isRealTime = true;

  // Mock sensor data - In real app, this would come from providers
  List<SensorData> _temperatureData = [];
  List<SensorData> _humidityData = [];
  List<SensorData> _phData = [];
  List<SensorData> _ecData = [];
  List<SensorData> _vpdData = []; // Added VPD Data

  @override
  void initState() {
    super.initState();
    _generateMockData();
    if (_isRealTime) {
      _startRealTimeUpdates();
    }
  }

  @override
  void dispose() {
    _pageController.dispose();
    super.dispose();
  }

  void _generateMockData() {
    final now = DateTime.now();
    final random = math.Random();

    // Generate temperature data (18-30°C)
    _temperatureData = List.generate(50, (index) {
      final time = now.subtract(Duration(minutes: (50 - index) * 10));
      return SensorData(
        timestamp: time,
        value: 20 + random.nextDouble() * 10 + math.sin(index / 5) * 2,
        unit: '°C',
        status: _getTemperatureStatus(20 + random.nextDouble() * 10),
      );
    });

    // Generate humidity data (40-80%)
    _humidityData = List.generate(50, (index) {
      final time = now.subtract(Duration(minutes: (50 - index) * 10));
      return SensorData(
        timestamp: time,
        value: 50 + random.nextDouble() * 20 + math.cos(index / 8) * 5,
        unit: '%',
        status: _getHumidityStatus(50 + random.nextDouble() * 20),
      );
    });

    // Generate VPD data (0.4 - 1.8 kPa)
    _vpdData = List.generate(50, (index) {
      final time = now.subtract(Duration(minutes: (50 - index) * 10));
      // Crude simulation: High temp + low humidity = High VPD
      final temp = _temperatureData[index].value;
      final hum = _humidityData[index].value;
      // Simplistic correlation for mock
      final mockVpd =
          (0.8 + (temp / 30) - (hum / 100)) + (random.nextDouble() * 0.2);

      return SensorData(
        timestamp: time,
        value: mockVpd.clamp(0.4, 2.0),
        unit: 'kPa',
        status: _getVpdStatus(mockVpd),
      );
    });

    // Generate pH data (5.5-7.0)
    _phData = List.generate(50, (index) {
      final time = now.subtract(Duration(minutes: (50 - index) * 10));
      return SensorData(
        timestamp: time,
        value: 5.8 + random.nextDouble() * 0.8 + math.sin(index / 12) * 0.1,
        unit: 'pH',
        status: _getPhStatus(5.8 + random.nextDouble() * 0.8),
      );
    });

    // Generate EC data (1.2-2.4 mS/cm)
    _ecData = List.generate(50, (index) {
      final time = now.subtract(Duration(minutes: (50 - index) * 10));
      return SensorData(
        timestamp: time,
        value: 1.6 + random.nextDouble() * 0.6 + math.cos(index / 15) * 0.1,
        unit: 'mS/cm',
        status: _getEcStatus(1.6 + random.nextDouble() * 0.6),
      );
    });
  }

  void _startRealTimeUpdates() {
    Future.delayed(const Duration(seconds: 5), () {
      if (mounted && _isRealTime) {
        _generateMockData();
        setState(() {});
        _startRealTimeUpdates();
      }
    });
  }

  SensorStatus _getTemperatureStatus(double value) {
    if (value < 18 || value > 30) return SensorStatus.alert;
    if (value < 20 || value > 28) return SensorStatus.warning;
    return SensorStatus.normal;
  }

  SensorStatus _getHumidityStatus(double value) {
    if (value < 40 || value > 80) return SensorStatus.alert;
    if (value < 45 || value > 75) return SensorStatus.warning;
    return SensorStatus.normal;
  }

  SensorStatus _getVpdStatus(double value) {
    if (value < 0.4 || value > 1.6) return SensorStatus.alert;
    if (value < 0.8 || value > 1.2) return SensorStatus.warning;
    return SensorStatus.normal;
  }

  SensorStatus _getPhStatus(double value) {
    if (value < 5.5 || value > 7.0) return SensorStatus.alert;
    if (value < 5.8 || value > 6.8) return SensorStatus.warning;
    return SensorStatus.normal;
  }

  SensorStatus _getEcStatus(double value) {
    if (value < 1.2 || value > 2.4) return SensorStatus.alert;
    if (value < 1.4 || value > 2.2) return SensorStatus.warning;
    return SensorStatus.normal;
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Environmental Sensors'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
        actions: [
          IconButton(
            icon: Icon(_isRealTime ? Icons.wifi : Icons.wifi_off),
            onPressed: () {
              setState(() {
                _isRealTime = !_isRealTime;
                if (_isRealTime) {
                  _startRealTimeUpdates();
                }
              });
            },
            tooltip: _isRealTime ? 'Real-time monitoring' : 'Offline mode',
          ),
          IconButton(
            icon: const Icon(Icons.download),
            onPressed: _exportData,
            tooltip: 'Export sensor data',
          ),
        ],
      ),
      body: Column(
        children: [
          _buildSensorOverview(),
          Expanded(
            child: PageView(
              controller: _pageController,
              onPageChanged: (index) {
                setState(() {
                  _currentPage = index;
                });
              },
              children: [
                _buildTemperatureChart(),
                _buildHumidityChart(),
                _buildVpdChart(), // Added VPD Chart
                _buildPhChart(),
                _buildEcChart(),
                _buildSensorStatusGrid(),
              ],
            ),
          ),
          _buildNavigationDots(),
          _buildTimeRangeSelector(),
        ],
      ),
    );
  }

  Widget _buildSensorOverview() {
    final currentData = <String, double>{
      'Temperature': _temperatureData.isNotEmpty
          ? _temperatureData.last.value
          : 0,
      'Humidity': _humidityData.isNotEmpty ? _humidityData.last.value : 0,
      'VPD': _vpdData.isNotEmpty ? _vpdData.last.value : 0, // Added VPD
      'pH': _phData.isNotEmpty ? _phData.last.value : 0,
      'EC': _ecData.isNotEmpty ? _ecData.last.value : 0,
    };

    return Container(
      height: 120,
      margin: const EdgeInsets.all(16),
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        itemCount: currentData.length,
        itemBuilder: (context, index) {
          final entry = currentData.entries.elementAt(index);
          final sensorType = entry.key;
          final value = entry.value;
          final status = _getCurrentStatus(sensorType, value);

          return Container(
            width: 160,
            margin: const EdgeInsets.only(right: 12),
            child: Card(
              elevation: 4,
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(
                          _getSensorIcon(sensorType),
                          color: _getStatusColor(status),
                          size: 20,
                        ),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            sensorType,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ),
                      ],
                    ),
                    const Spacer(),
                    Text(
                      _formatSensorValue(sensorType, value),
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: _getStatusColor(status),
                      ),
                    ),
                    Text(
                      _getStatusText(status),
                      style: TextStyle(
                        fontSize: 11,
                        color: _getStatusColor(status).withOpacity(0.8),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildTemperatureChart() {
    return _buildChartCard(
      title: 'Temperature',
      icon: Icons.thermostat,
      data: _temperatureData,
      color: Colors.red,
      unit: '°C',
      minValue: 15,
      maxValue: 35,
    );
  }

  Widget _buildHumidityChart() {
    return _buildChartCard(
      title: 'Humidity',
      icon: Icons.water_drop,
      data: _humidityData,
      color: Colors.blue,
      unit: '%',
      minValue: 30,
      maxValue: 90,
    );
  }

  Widget _buildVpdChart() {
    return _buildChartCard(
      title: 'VPD',
      icon: Icons.cloud_queue, // Use a cloud icon for VPD
      data: _vpdData,
      color: Colors.teal,
      unit: 'kPa',
      minValue: 0,
      maxValue: 2.5,
    );
  }

  Widget _buildPhChart() {
    return _buildChartCard(
      title: 'pH Level',
      icon: Icons.science,
      data: _phData,
      color: Colors.purple,
      unit: 'pH',
      minValue: 5.0,
      maxValue: 8.0,
    );
  }

  Widget _buildEcChart() {
    return _buildChartCard(
      title: 'Electrical Conductivity',
      icon: Icons.electrical_services,
      data: _ecData,
      color: Colors.orange,
      unit: 'mS/cm',
      minValue: 0.5,
      maxValue: 3.0,
    );
  }

  Widget _buildChartCard({
    required String title,
    required IconData icon,
    required List<SensorData> data,
    required Color color,
    required String unit,
    required double minValue,
    required double maxValue,
  }) {
    if (data.isEmpty) {
      return const Center(child: CircularProgressIndicator());
    }

    final spots = data.asMap().entries.map((entry) {
      return FlSpot(entry.key.toDouble(), entry.value.value);
    }).toList();

    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 24),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const Spacer(),
                Text(
                  '${data.last.value.toStringAsFixed(1)} $unit',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: color,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 16),
            Expanded(
              child: LineChart(
                LineChartData(
                  gridData: const FlGridData(show: false),
                  titlesData: FlTitlesData(
                    bottomTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 40,
                        getTitlesWidget: (value, meta) {
                          if (value.toInt() % 10 == 0 &&
                              value.toInt() < data.length) {
                            final time = data[value.toInt()].timestamp;
                            return Text(
                              '${time.hour}:${time.minute.toString().padLeft(2, '0')}',
                              style: const TextStyle(fontSize: 10),
                            );
                          }
                          return const Text('');
                        },
                      ),
                    ),
                    leftTitles: AxisTitles(
                      sideTitles: SideTitles(
                        showTitles: true,
                        reservedSize: 50,
                        getTitlesWidget: (value, meta) {
                          return Text(
                            value.toStringAsFixed(
                              1,
                            ), // Changed to 1 decimal for VPD precision
                            style: const TextStyle(fontSize: 10),
                          );
                        },
                      ),
                    ),
                    rightTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                    topTitles: const AxisTitles(
                      sideTitles: SideTitles(showTitles: false),
                    ),
                  ),
                  borderData: FlBorderData(show: false),
                  minX: 0,
                  maxX: data.length - 1.0,
                  minY: minValue,
                  maxY: maxValue,
                  lineTouchData: LineTouchData(
                    enabled: true,
                    touchCallback:
                        (FlTouchEvent event, LineTouchResponse? touchResponse) {
                          if (touchResponse != null &&
                              touchResponse.lineBarSpots != null) {
                            final spot = touchResponse.lineBarSpots!.first;
                            final dataPoint = data[spot.x.toInt()];
                            AppLogger.log(
                              '$title: ${dataPoint.value.toStringAsFixed(2)} $unit at ${dataPoint.timestamp}',
                            );
                          }
                        },
                  ),
                  lineBarsData: [
                    LineChartBarData(
                      spots: spots,
                      isCurved: true,
                      color: color,
                      barWidth: 3,
                      isStrokeCapRound: true,
                      dotData: const FlDotData(show: false),
                      belowBarData: BarAreaData(
                        show: true,
                        gradient: LinearGradient(
                          begin: Alignment.topCenter,
                          end: Alignment.bottomCenter,
                          colors: [
                            color.withOpacity(0.3),
                            color.withOpacity(0.05),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildSensorStatusGrid() {
    final sensors = [
      {
        'name': 'Temperature',
        'value': _temperatureData.isNotEmpty ? _temperatureData.last.value : 0,
        'unit': '°C',
        'status': _temperatureData.isNotEmpty
            ? _temperatureData.last.status
            : SensorStatus.normal,
        'icon': Icons.thermostat,
      },
      {
        'name': 'Humidity',
        'value': _humidityData.isNotEmpty ? _humidityData.last.value : 0,
        'unit': '%',
        'status': _humidityData.isNotEmpty
            ? _humidityData.last.status
            : SensorStatus.normal,
        'icon': Icons.water_drop,
      },
      {
        'name': 'VPD', // Added VPD
        'value': _vpdData.isNotEmpty ? _vpdData.last.value : 0,
        'unit': 'kPa',
        'status': _vpdData.isNotEmpty
            ? _vpdData.last.status
            : SensorStatus.normal,
        'icon': Icons.cloud_queue,
      },
      {
        'name': 'pH Level',
        'value': _phData.isNotEmpty ? _phData.last.value : 0,
        'unit': 'pH',
        'status': _phData.isNotEmpty
            ? _phData.last.status
            : SensorStatus.normal,
        'icon': Icons.science,
      },
      {
        'name': 'EC',
        'value': _ecData.isNotEmpty ? _ecData.last.value : 0,
        'unit': 'mS/cm',
        'status': _ecData.isNotEmpty
            ? _ecData.last.status
            : SensorStatus.normal,
        'icon': Icons.electrical_services,
      },
      {
        'name': 'Light',
        'value': 450,
        'unit': 'lux',
        'status': SensorStatus.normal,
        'icon': Icons.lightbulb,
      },
      {
        'name': 'CO2',
        'value': 850,
        'unit': 'ppm',
        'status': SensorStatus.alert,
        'icon': Icons.cloud,
      },
    ];

    return Padding(
      padding: const EdgeInsets.all(16),
      child: GridView.builder(
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          childAspectRatio: 1.2,
          crossAxisSpacing: 12,
          mainAxisSpacing: 12,
        ),
        itemCount: sensors.length,
        itemBuilder: (context, index) {
          final sensor = sensors[index];
          return Card(
            elevation: 4,
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(
                    sensor['icon'] as IconData,
                    size: 32,
                    color: _getStatusColor(sensor['status'] as SensorStatus),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    sensor['name'] as String,
                    style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w600,
                    ),
                    textAlign: TextAlign.center,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${(sensor['value'] as num).toStringAsFixed(sensor['unit'] == 'kPa' ? 2 : 1)} ${sensor['unit']}',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: _getStatusColor(sensor['status'] as SensorStatus),
                    ),
                  ),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 2,
                    ),
                    decoration: BoxDecoration(
                      color: _getStatusColor(
                        sensor['status'] as SensorStatus,
                      ).withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      _getStatusText(sensor['status'] as SensorStatus),
                      style: TextStyle(
                        fontSize: 10,
                        color: _getStatusColor(
                          sensor['status'] as SensorStatus,
                        ),
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildNavigationDots() {
    return Container(
      height: 40,
      alignment: Alignment.center,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        shrinkWrap: true,
        itemCount: 6, // Increased count to 6 (Temp, Hum, VPD, pH, EC, Grid)
        itemBuilder: (context, index) {
          return GestureDetector(
            onTap: () {
              _pageController.animateToPage(
                index,
                duration: const Duration(milliseconds: 300),
                curve: Curves.easeInOut,
              );
            },
            child: Container(
              width: 12,
              height: 12,
              margin: const EdgeInsets.symmetric(horizontal: 4),
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _currentPage == index
                    ? Theme.of(context).primaryColor
                    : Colors.grey.withOpacity(0.5),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildTimeRangeSelector() {
    return Container(
      height: 60,
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          const Text('Time Range:'),
          const SizedBox(width: 16),
          Expanded(
            child: ListView.builder(
              scrollDirection: Axis.horizontal,
              itemCount: _timeRanges.length,
              itemBuilder: (context, index) {
                return GestureDetector(
                  onTap: () {
                    setState(() {
                      _selectedTimeRange = index;
                    });
                    AppLogger.log(
                      'Changed time range to: ${_timeRanges[index]}',
                    );
                  },
                  child: Container(
                    margin: const EdgeInsets.only(right: 8),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 8,
                    ),
                    decoration: BoxDecoration(
                      color: _selectedTimeRange == index
                          ? Theme.of(context).primaryColor
                          : Colors.grey.withOpacity(0.3),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      _timeRanges[index],
                      style: TextStyle(
                        color: _selectedTimeRange == index
                            ? Colors.white
                            : Theme.of(context).textTheme.bodyMedium?.color,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  String _formatSensorValue(String sensorType, double value) {
    switch (sensorType) {
      case 'Temperature':
        return '${value.toStringAsFixed(1)}°C';
      case 'Humidity':
        return '${value.toStringAsFixed(1)}%';
      case 'VPD': // Added VPD
        return '${value.toStringAsFixed(2)} kPa';
      case 'pH':
        return value.toStringAsFixed(2);
      case 'EC':
        return '${value.toStringAsFixed(2)} mS/cm';
      default:
        return value.toStringAsFixed(1);
    }
  }

  IconData _getSensorIcon(String sensorType) {
    switch (sensorType) {
      case 'Temperature':
        return Icons.thermostat;
      case 'Humidity':
        return Icons.water_drop;
      case 'VPD': // Added VPD
        return Icons.cloud_queue;
      case 'pH':
        return Icons.science;
      case 'EC':
        return Icons.electrical_services;
      case 'Light':
        return Icons.lightbulb;
      case 'CO2':
        return Icons.cloud;
      default:
        return Icons.sensors;
    }
  }

  SensorStatus _getCurrentStatus(String sensorType, double value) {
    switch (sensorType) {
      case 'Temperature':
        return _getTemperatureStatus(value);
      case 'Humidity':
        return _getHumidityStatus(value);
      case 'VPD': // Added VPD
        return _getVpdStatus(value);
      case 'pH':
        return _getPhStatus(value);
      case 'EC':
        return _getEcStatus(value);
      default:
        return SensorStatus.normal;
    }
  }

  Color _getStatusColor(SensorStatus status) {
    switch (status) {
      case SensorStatus.normal:
        return Colors.green;
      case SensorStatus.warning:
        return Colors.orange;
      case SensorStatus.alert:
        return Colors.red;
    }
  }

  String _getStatusText(SensorStatus status) {
    switch (status) {
      case SensorStatus.normal:
        return 'Normal';
      case SensorStatus.warning:
        return 'Warning';
      case SensorStatus.alert:
        return 'Alert';
    }
  }

  void _exportData() {
    // Mock export functionality
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Sensor data export started...'),
        duration: Duration(seconds: 2),
      ),
    );
    AppLogger.log('Sensor data export initiated');
  }
}

/// Sensor data model
class SensorData {
  const SensorData({
    required this.timestamp,
    required this.value,
    required this.unit,
    required this.status,
  });
  final DateTime timestamp;
  final double value;
  final String unit;
  final SensorStatus status;
}

/// Sensor status enumeration
enum SensorStatus { normal, warning, alert }
