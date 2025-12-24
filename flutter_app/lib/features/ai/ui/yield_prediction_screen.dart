import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../services/agent_api_client.dart';
import '../../admin/widgets/admin_scaffold.dart';

class YieldPredictionScreen extends ConsumerStatefulWidget {
  const YieldPredictionScreen({super.key});

  @override
  ConsumerState<YieldPredictionScreen> createState() =>
      _YieldPredictionScreenState();
}

class _YieldPredictionScreenState extends ConsumerState<YieldPredictionScreen> {
  final _formKey = GlobalKey<FormState>();

  // Inputs
  double _lightWatts = 400;
  double _spaceSqFt = 16; // 4x4 tent
  double _vegWeeks = 4;
  String _experienceLevel = 'intermediate';
  final String _strainType = 'photoperiod';

  bool _isLoading = false;
  Map<String, dynamic>? _result;
  String? _error;

  final List<String> _experienceLevels = [
    'beginner',
    'intermediate',
    'advanced',
    'master',
  ];

  Future<void> _calculateYield() async {
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();

    setState(() {
      _isLoading = true;
      _error = null;
      _result = null;
    });

    try {
      final response = await ref
          .read(agentApiClientProvider)
          .executeAgent('yield_estimator', 'estimate', {
            'light_watts': _lightWatts.toInt(),
            'space_sqft': _spaceSqFt,
            'experience': _experienceLevel,
            'veg_weeks': _vegWeeks.toInt(),
            'strain_type': _strainType,
          });

      if (mounted) {
        setState(() {
          _result = response['result'] as Map<String, dynamic>;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = e.toString();
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AdminScaffold(
      title: 'Yield Prediction',
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Input Card
            Card(
              color: AppColors.adminCard,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        'Grow Parameters',
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 20),

                      // Light Watts
                      Text(
                        'Light Wattage (True Draw): ${_lightWatts.toInt()}W',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Slider(
                        value: _lightWatts,
                        min: 50,
                        max: 2000,
                        divisions: 195,
                        label: '${_lightWatts.toInt()}W',
                        activeColor: AppColors.primary500,
                        onChanged: (val) => setState(() => _lightWatts = val),
                      ),

                      const SizedBox(height: 10),

                      // Space
                      Text(
                        'Grow Space: ${_spaceSqFt.toStringAsFixed(1)} sq ft',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Slider(
                        value: _spaceSqFt,
                        min: 2,
                        max: 100,
                        divisions: 49,
                        label: '${_spaceSqFt.toStringAsFixed(1)} sq ft',
                        activeColor: AppColors.primary500,
                        onChanged: (val) => setState(() => _spaceSqFt = val),
                      ),

                      const SizedBox(height: 10),

                      // Veg Weeks
                      Text(
                        'Vegetative Time: ${_vegWeeks.toInt()} Weeks',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Slider(
                        value: _vegWeeks,
                        min: 1,
                        max: 12,
                        divisions: 11,
                        label: '${_vegWeeks.toInt()} Weeks',
                        activeColor: AppColors.primary500,
                        onChanged: (val) => setState(() => _vegWeeks = val),
                      ),

                      const SizedBox(height: 16),

                      // Experience Level
                      DropdownButtonFormField<String>(
                        initialValue: _experienceLevel,
                        decoration: _inputDecoration('Experience Level'),
                        dropdownColor: AppColors.adminSurface,
                        style: const TextStyle(color: Colors.white),
                        items: _experienceLevels.map((lvl) {
                          return DropdownMenuItem(
                            value: lvl,
                            child: Text(
                              lvl[0].toUpperCase() + lvl.substring(1),
                            ),
                          );
                        }).toList(),
                        onChanged: (val) =>
                            setState(() => _experienceLevel = val!),
                      ),

                      const SizedBox(height: 24),

                      SizedBox(
                        width: double.infinity,
                        child: ElevatedButton.icon(
                          onPressed: _isLoading ? null : _calculateYield,
                          icon: _isLoading
                              ? const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(
                                    strokeWidth: 2,
                                  ),
                                )
                              : const Icon(Icons.analytics_outlined),
                          label: Text(
                            _isLoading ? 'Estimating...' : 'Estimate Yield',
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
            ),

            if (_error != null)
              Container(
                margin: const EdgeInsets.only(top: 16),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.danger.withOpacity(0.1),
                  border: Border.all(color: AppColors.danger),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  _error!,
                  style: const TextStyle(color: AppColors.danger),
                ),
              ),

            // Results Area
            if (_result != null) ...[
              const SizedBox(height: 20),
              _buildResultsCard(_result!),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildResultsCard(Map<String, dynamic> data) {
    final grams = data['estimated_yield_grams'] as Map<String, dynamic>;
    final ounces = data['estimated_yield_ounces'] as Map<String, dynamic>;
    final efficiency = data['efficiency_rating'] as String;

    return Card(
      color: AppColors.adminCard,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Text(
              'Harvest Potential',
              style: TextStyle(
                color: AppColors.primary500,
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 20),

            // Targets
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildStatColumn(
                  'Min Estimate',
                  '${grams['min']}g\n(${ounces['min']}oz)',
                ),
                Container(width: 1, height: 40, color: Colors.white24),
                _buildStatColumn(
                  'Target Yield',
                  '${grams['target']}g\n(${ounces['target']}oz)',
                  isPrimary: true,
                ),
                Container(width: 1, height: 40, color: Colors.white24),
                _buildStatColumn(
                  'Max Potential',
                  '${grams['max']}g\n(${ounces['max']}oz)',
                ),
              ],
            ),

            const Divider(color: Colors.white24, height: 30),

            Text(
              'Efficiency Rating: $efficiency',
              style: const TextStyle(
                color: Colors.white70,
                fontStyle: FontStyle.italic,
              ),
            ),

            if (data['limiting_factors'] != null) ...[
              const SizedBox(height: 16),
              Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Factors to Improve:',
                  style: TextStyle(
                    color: Colors.orange[300],
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
              const SizedBox(height: 8),
              ...(data['limiting_factors'] as List).map(
                (f) => Padding(
                  padding: const EdgeInsets.only(bottom: 4),
                  child: Row(
                    children: [
                      const Icon(
                        Icons.arrow_right,
                        color: Colors.orange,
                        size: 16,
                      ),
                      Text(f, style: const TextStyle(color: Colors.white70)),
                    ],
                  ),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatColumn(
    String label,
    String value, {
    bool isPrimary = false,
  }) {
    return Column(
      children: [
        Text(
          label,
          style: const TextStyle(color: Colors.white60, fontSize: 12),
        ),
        const SizedBox(height: 4),
        Text(
          value,
          textAlign: TextAlign.center,
          style: TextStyle(
            color: isPrimary ? AppColors.primary500 : Colors.white,
            fontSize: isPrimary ? 22 : 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ],
    );
  }

  InputDecoration _inputDecoration(String label) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.white70),
      enabledBorder: OutlineInputBorder(
        borderSide: const BorderSide(color: Colors.white24),
        borderRadius: BorderRadius.circular(8),
      ),
      focusedBorder: OutlineInputBorder(
        borderSide: const BorderSide(color: AppColors.primary500),
        borderRadius: BorderRadius.circular(8),
      ),
    );
  }
}
