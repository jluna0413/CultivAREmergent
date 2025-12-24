import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/providers/api_client_provider.dart';
import '../../../core/services/nutrients_service.dart';

/// Provider for nutrients API service
final nutrientsServiceProvider = Provider<NutrientsApiService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return NutrientsApiService(apiClient);
});

/// Provider for nutrient brands
final nutrientBrandsProvider = FutureProvider<List<NutrientBrand>>((ref) async {
  final service = ref.watch(nutrientsServiceProvider);
  return await service.getBrands();
});

/// Nutrient Calculator Screen
class NutrientCalculatorScreen extends ConsumerStatefulWidget {
  const NutrientCalculatorScreen({super.key});

  @override
  ConsumerState<NutrientCalculatorScreen> createState() =>
      _NutrientCalculatorScreenState();
}

class _NutrientCalculatorScreenState
    extends ConsumerState<NutrientCalculatorScreen> {
  NutrientBrand? _selectedBrand;
  String _growthStage = 'early_veg';
  String _medium = 'hydro';
  double _tankSize = 10.0;
  String _feedingStrength = 'medium';
  String _waterType = 'tap';
  NutrientMix? _calculatedMix;
  bool _isCalculating = false;

  final List<Map<String, String>> _growthStages = [
    {'value': 'seedling', 'label': 'Seedling'},
    {'value': 'early_veg', 'label': 'Early Veg'},
    {'value': 'late_veg', 'label': 'Late Veg'},
    {'value': 'early_flower', 'label': 'Early Flower'},
    {'value': 'mid_flower', 'label': 'Mid Flower'},
    {'value': 'late_flower', 'label': 'Late Flower'},
    {'value': 'flush', 'label': 'Flush'},
  ];

  final List<Map<String, String>> _mediums = [
    {'value': 'hydro', 'label': 'Hydroponic'},
    {'value': 'coco', 'label': 'Coco Coir'},
    {'value': 'soil', 'label': 'Soil'},
    {'value': 'inert', 'label': 'Inert (Perlite/Rockwool)'},
  ];

  final List<Map<String, String>> _strengths = [
    {'value': 'light', 'label': 'Light (50%)'},
    {'value': 'medium', 'label': 'Medium (75%)'},
    {'value': 'aggressive', 'label': 'Aggressive (100%)'},
  ];

  final List<Map<String, String>> _waterTypes = [
    {'value': 'tap', 'label': 'Tap Water'},
    {'value': 'distilled', 'label': 'Distilled'},
    {'value': 'ro', 'label': 'Reverse Osmosis (RO)'},
    {'value': 're_mineralized', 'label': 'RO + Re-Mineralized'},
  ];

  Future<void> _calculateMix() async {
    if (_selectedBrand == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please select a nutrient brand')),
      );
      return;
    }

    setState(() => _isCalculating = true);

    try {
      final service = ref.read(nutrientsServiceProvider);
      final mix = await service.calculateMix(
        brandId: _selectedBrand!.id,
        growthStage: _growthStage,
        medium: _medium,
        tankSizeLiters: _tankSize,
        feedingStrength: _feedingStrength,
        waterType: _waterType,
      );

      setState(() {
        _calculatedMix = mix;
        _isCalculating = false;
      });
    } catch (e) {
      setState(() => _isCalculating = false);
      if (mounted) {
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final brandsAsync = ref.watch(nutrientBrandsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Nutrient Calculator'),
        actions: [
          IconButton(
            icon: const Icon(Icons.inventory),
            onPressed: () {
              // TODO: Navigate to inventory screen
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Inventory screen coming soon!')),
              );
            },
            tooltip: 'My Inventory',
          ),
        ],
      ),
      body: brandsAsync.when(
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) =>
            Center(child: Text('Error loading brands: $error')),
        data: (brands) => SingleChildScrollView(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _buildBrandSelector(brands),
              const SizedBox(height: 16),
              _buildParametersCard(),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _isCalculating ? null : _calculateMix,
                icon: _isCalculating
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.calculate),
                label: Text(
                  _isCalculating ? 'Calculating...' : 'Calculate Mix',
                ),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                ),
              ),
              if (_calculatedMix != null) ...[
                const SizedBox(height: 24),
                _buildResultsCard(_calculatedMix!),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildBrandSelector(List<NutrientBrand> brands) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Nutrient Brand',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            DropdownButtonFormField<NutrientBrand>(
              initialValue: _selectedBrand,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Select brand',
              ),
              items: brands.map((brand) {
                return DropdownMenuItem(
                  value: brand,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(
                        brand.name,
                        style: const TextStyle(fontWeight: FontWeight.w500),
                      ),
                      if (brand.manufacturer != null)
                        Text(
                          brand.manufacturer!,
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey[600],
                          ),
                        ),
                    ],
                  ),
                );
              }).toList(),
              onChanged: (value) => setState(() => _selectedBrand = value),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildParametersCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Parameters',
              style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            _buildDropdown(
              'Growth Stage',
              _growthStage,
              _growthStages,
              (v) => setState(() => _growthStage = v!),
            ),
            const SizedBox(height: 12),
            _buildDropdown(
              'Growing Medium',
              _medium,
              _mediums,
              (v) => setState(() => _medium = v!),
            ),
            const SizedBox(height: 12),
            _buildDropdown(
              'Water Type',
              _waterType,
              _waterTypes,
              (v) => setState(() => _waterType = v!),
            ),
            const SizedBox(height: 12),
            _buildDropdown(
              'Feeding Strength',
              _feedingStrength,
              _strengths,
              (v) => setState(() => _feedingStrength = v!),
            ),
            const SizedBox(height: 16),
            Text('Tank Size: ${_tankSize.toStringAsFixed(1)}L'),
            Slider(
              value: _tankSize,
              min: 1.0,
              max: 100.0,
              divisions: 99,
              label: '${_tankSize.toStringAsFixed(1)}L',
              onChanged: (value) => setState(() => _tankSize = value),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDropdown(
    String label,
    String value,
    List<Map<String, String>> items,
    void Function(String?) onChanged,
  ) {
    return DropdownButtonFormField<String>(
      initialValue: value,
      decoration: InputDecoration(
        labelText: label,
        border: const OutlineInputBorder(),
      ),
      items: items.map((item) {
        return DropdownMenuItem(
          value: item['value'],
          child: Text(item['label']!),
        );
      }).toList(),
      onChanged: onChanged,
    );
  }

  Widget _buildResultsCard(NutrientMix mix) {
    return Card(
      color: mix.inventorySufficient ? Colors.green[50] : Colors.orange[50],
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Row(
              children: [
                Icon(Icons.science, size: 28),
                SizedBox(width: 8),
                Text(
                  'Your Nutrient Mix',
                  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                ),
              ],
            ),
            const Divider(height: 24),

            // Components
            const Text(
              'Components:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...mix.components.entries.map((entry) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(entry.key),
                    Text(
                      '${entry.value.toStringAsFixed(1)} ml',
                      style: const TextStyle(fontWeight: FontWeight.w500),
                    ),
                  ],
                ),
              );
            }),

            if (mix.requiresCalmag && mix.calmagMl != null) ...[
              const Divider(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    'CalMag Supplement',
                    style: TextStyle(color: Colors.orange),
                  ),
                  Text(
                    '${mix.calmagMl!.toStringAsFixed(1)} ml',
                    style: const TextStyle(fontWeight: FontWeight.w500),
                  ),
                ],
              ),
            ],

            const Divider(height: 24),

            // Targets
            Wrap(
              spacing: 16,
              runSpacing: 8,
              children: [
                _buildTargetChip(
                  'PPM',
                  '${mix.ppmTarget.$1.toInt()}-${mix.ppmTarget.$2.toInt()}',
                ),
                _buildTargetChip(
                  'EC',
                  '${mix.ecTarget.$1.toStringAsFixed(1)}-${mix.ecTarget.$2.toStringAsFixed(1)}',
                ),
                _buildTargetChip(
                  'pH',
                  '${mix.phTarget.$1.toStringAsFixed(1)}-${mix.phTarget.$2.toStringAsFixed(1)}',
                ),
              ],
            ),

            if (!mix.inventorySufficient) ...[
              const Divider(height: 24),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: Colors.orange[100],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.warning, color: Colors.orange, size: 20),
                        SizedBox(width: 8),
                        Text(
                          'Insufficient Inventory',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    ...mix.insufficientItems.map((item) => Text('• $item')),
                  ],
                ),
              ),
            ],

            if (mix.estimatedCost != null) ...[
              const Divider(height: 16),
              Text(
                'Estimated Cost: \$${mix.estimatedCost!.toStringAsFixed(2)}',
              ),
            ],

            const Divider(height: 24),

            // Mixing Instructions
            const Text(
              'Mixing Instructions:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            ...mix.mixingInstructions.asMap().entries.map((entry) {
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Container(
                      width: 24,
                      height: 24,
                      decoration: BoxDecoration(
                        color: Theme.of(context).primaryColor,
                        shape: BoxShape.circle,
                      ),
                      child: Center(
                        child: Text(
                          '${entry.key + 1}',
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(child: Text(entry.value)),
                  ],
                ),
              );
            }),
          ],
        ),
      ),
    );
  }

  Widget _buildTargetChip(String label, String value) {
    return Chip(
      label: Text('$label: $value'),
      backgroundColor: Colors.blue[100],
    );
  }
}
