import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../services/agent_api_client.dart';
import '../../admin/widgets/admin_scaffold.dart';

class EnvironmentalInsightsScreen extends ConsumerStatefulWidget {
  const EnvironmentalInsightsScreen({super.key});

  @override
  ConsumerState<EnvironmentalInsightsScreen> createState() =>
      _EnvironmentalInsightsScreenState();
}

class _EnvironmentalInsightsScreenState
    extends ConsumerState<EnvironmentalInsightsScreen> {
  // Environmental Inputs
  double _temperature = 75.0;
  double _humidity = 55.0;
  final double _leafOffset = -2.0;
  String _growthStage = 'late_veg';

  // State
  bool _isLoading = false;
  Map<String, dynamic>? _result;
  String? _error;

  final List<String> _growthStages = [
    'seedling',
    'early_veg',
    'late_veg',
    'early_flower',
    'mid_flower',
    'late_flower',
    'ripening',
  ];

  @override
  void initState() {
    super.initState();
    // Initial optimization run
    WidgetsBinding.instance.addPostFrameCallback((_) => _optimizeVpd());
  }

  Future<void> _optimizeVpd() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final result = await ref.read(agentApiClientProvider).executeAgent(
        'vpd_optimizer',
        'recommend',
        {
          'temperature': _temperature,
          'humidity': _humidity,
          'growth_stage': _growthStage,
          // 'leaf_temp_offset': _leafOffset, // Agent might not take this for 'recommend' but 'calculate' does.
          // Let's actually call 'calculate' first to get precision data, or just trust 'recommend'.
          // 'recommend' calls 'calculate' internally if params provided.
        },
      );

      if (mounted) {
        setState(() {
          // The result structure from 'recommend' action:
          // { "result": { "current_vpd": ..., "recommendations": [], "summary": ... } }
          _result = result['result'] as Map<String, dynamic>?;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _error = 'Optimization failed: $e');
      }
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  Color _getVpdColor(double vpd, Map<String, dynamic>? range) {
    if (range == null) return Colors.grey;
    final min = range['min'] as double;
    final max = range['max'] as double;

    if (vpd >= min && vpd <= max) return AppColors.success;
    if (vpd < min - 0.4 || vpd > max + 0.4) return AppColors.danger;
    return AppColors.warning;
  }

  @override
  Widget build(BuildContext context) {
    return AdminScaffold(
      title: '🌡️ VPD Optimizer',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Controls Card
            Card(
              color: AppColors.adminCard,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Environmental Conditions',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Temperature Slider
                    _buildSlider(
                      'Temperature',
                      '${_temperature.toStringAsFixed(1)}°F',
                      _temperature,
                      60,
                      95,
                      (val) => setState(() => _temperature = val),
                    ),

                    // Humidity Slider
                    _buildSlider(
                      'Humidity',
                      '${_humidity.toStringAsFixed(0)}%',
                      _humidity,
                      30,
                      90,
                      (val) => setState(() => _humidity = val),
                    ),

                    // Growth Stage Dropdown
                    DropdownButtonFormField<String>(
                      initialValue: _growthStage,
                      decoration: const InputDecoration(
                        labelText: 'Growth Stage',
                        border: OutlineInputBorder(),
                        filled: true,
                        fillColor: Colors.black26,
                      ),
                      dropdownColor: AppColors.adminCard,
                      items: _growthStages
                          .map(
                            (s) => DropdownMenuItem(
                              value: s,
                              child: Text(
                                s.replaceAll('_', ' ').toUpperCase(),
                                style: const TextStyle(color: Colors.white),
                              ),
                            ),
                          )
                          .toList(),
                      onChanged: (val) {
                        if (val != null) setState(() => _growthStage = val);
                      },
                    ),
                    const SizedBox(height: 16),

                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        onPressed: _isLoading ? null : _optimizeVpd,
                        icon: _isLoading
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: Colors.white,
                                ),
                              )
                            : const Icon(Icons.analytics),
                        label: Text(
                          _isLoading ? 'Optimizing...' : 'Calculate & Optimize',
                        ),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppColors.primary500,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 16),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),

            const SizedBox(height: 24),

            // Error Display
            if (_error != null)
              Container(
                padding: const EdgeInsets.all(16),
                color: AppColors.danger.withOpacity(0.1),
                child: Text(
                  _error!,
                  style: const TextStyle(color: AppColors.danger),
                ),
              ),

            // Results Display
            if (_result != null) ...[
              _buildResultsDisplay(_result!),
              const SizedBox(height: 24),
              if (_result!['recommendations'] != null)
                _buildRecommendationsList(
                  _result!['recommendations'] as List<dynamic>,
                ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildSlider(
    String label,
    String valueText,
    double value,
    double min,
    double max,
    ValueChanged<double> onChanged,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label, style: const TextStyle(color: Colors.grey)),
            Text(
              valueText,
              style: const TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
        Slider(
          value: value,
          min: min,
          max: max,
          activeColor: AppColors.primary500,
          inactiveColor: Colors.grey[800],
          onChanged: onChanged,
        ),
        const SizedBox(height: 8),
      ],
    );
  }

  Widget _buildResultsDisplay(Map<String, dynamic> result) {
    final currentVpd = result['current_vpd'] as double;
    final range = result['optimal_range'];
    final summary = result['summary'] as String?;
    final color = _getVpdColor(currentVpd, range);

    return Card(
      color: AppColors.adminCard,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          children: [
            Text(
              'Current VPD',
              style: TextStyle(color: Colors.grey[400], fontSize: 14),
            ),
            const SizedBox(height: 8),
            Text(
              '${currentVpd.toStringAsFixed(2)} kPa',
              style: TextStyle(
                color: color,
                fontSize: 48,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.black26,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Text(
                'Goal: ${range['min']} - ${range['max']} kPa',
                style: const TextStyle(color: Colors.grey, fontSize: 12),
              ),
            ),
            if (summary != null) ...[
              const SizedBox(height: 20),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: color.withOpacity(0.3)),
                ),
                child: Text(
                  summary,
                  textAlign: TextAlign.center,
                  style: TextStyle(color: Colors.grey[300]),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildRecommendationsList(List<dynamic> recommendations) {
    if (recommendations.isEmpty) return const SizedBox.shrink();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Optimization Plan',
          style: TextStyle(
            color: Colors.white,
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 12),
        ...recommendations.map((rec) => _buildRecommendationCard(rec)),
      ],
    );
  }

  Widget _buildRecommendationCard(Map<String, dynamic> rec) {
    final action = rec['action'] as String;
    final isIncrease = action.contains('increase');
    final icon = isIncrease ? Icons.arrow_upward : Icons.arrow_downward;
    final color = rec['priority'] == 'high' ? AppColors.danger : AppColors.info;

    return Card(
      color: AppColors.adminCard,
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: color.withOpacity(0.1),
          child: Icon(icon, color: color, size: 20),
        ),
        title: Text(
          rec['explanation'] ?? '',
          style: const TextStyle(color: Colors.white, fontSize: 14),
        ),
        subtitle: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const SizedBox(height: 4),
            if (rec['methods'] != null)
              ...(rec['methods'] as List).map(
                (m) => Row(
                  children: [
                    const Icon(Icons.circle, size: 6, color: Colors.grey),
                    const SizedBox(width: 8),
                    Text(
                      m,
                      style: TextStyle(color: Colors.grey[400], fontSize: 12),
                    ),
                  ],
                ),
              ),
          ],
        ),
      ),
    );
  }
}
