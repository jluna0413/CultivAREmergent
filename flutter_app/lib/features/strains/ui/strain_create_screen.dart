import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_navigation_drawer.dart';
import '../domain/strain_model.dart';
import '../providers/strains_providers.dart';
import 'widgets/genetics_slider.dart';

class StrainCreateScreen extends ConsumerStatefulWidget {
  const StrainCreateScreen({super.key});

  @override
  ConsumerState<StrainCreateScreen> createState() => _StrainCreateScreenState();
}

class _StrainCreateScreenState extends ConsumerState<StrainCreateScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _descriptionController = TextEditingController();
  final _breederController = TextEditingController();
  final _floweringTimeController = TextEditingController();
  final _referenceUrlController = TextEditingController();

  int _indicaPercentage = 50;
  int _sativaPercentage = 50;
  bool _autoflower = false;
  bool _isLoading = false;

  @override
  void dispose() {
    _nameController.dispose();
    _descriptionController.dispose();
    _breederController.dispose();
    _floweringTimeController.dispose();
    _referenceUrlController.dispose();
    super.dispose();
  }

  Future<void> _handleCreateStrain() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      // Create strain data using the CultivarCreate model
      final cultivarCreate = CultivarCreate(
        name: _nameController.text.trim(),
        description: _descriptionController.text.trim().isNotEmpty
            ? _descriptionController.text.trim()
            : null,
        indica: _indicaPercentage,
        sativa: _sativaPercentage,
        ruderalis: 0,
        floweringType: _autoflower ? 'autoflower' : 'photoperiod',
        floweringDays: _floweringTimeController.text.trim().isNotEmpty
            ? int.tryParse(_floweringTimeController.text)
            : null,
      );

      // Use the mutation provider to create the strain
      await ref.read(createStrainMutationProvider(cultivarCreate).future);

      if (mounted) {
        // Show success message
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(
              'Strain "${_nameController.text}" created successfully!',
            ),
            backgroundColor: Colors.green,
          ),
        );

        // Navigate back
        Navigator.of(context).pop(true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error creating strain: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create New Strain'),
        backgroundColor: AppColors.primary500,
        foregroundColor: Colors.white,
        actions: [
          TextButton(
            onPressed: _isLoading ? null : _handleCreateStrain,
            child: Text(
              'Save',
              style: TextStyle(
                color: _isLoading ? Colors.grey[300] : Colors.white,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
        ],
      ),
      drawer: const AppNavigationDrawer(),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Basic Information
              _buildSectionHeader('Basic Information'),
              const SizedBox(height: 16),

              TextFormField(
                controller: _nameController,
                decoration: InputDecoration(
                  labelText: 'Strain Name *',
                  labelStyle: const TextStyle(color: Colors.white),
                  prefixIcon: const Icon(Icons.eco, color: Colors.white),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: AppColors.primary500),
                  ),
                  filled: true,
                  fillColor: const Color(0xFF2a2a2a),
                ),
                style: const TextStyle(color: Colors.white),
                validator: (value) {
                  if (value == null || value.trim().isEmpty) {
                    return 'Please enter a strain name';
                  }
                  return null;
                },
              ),

              const SizedBox(height: 16),

              TextFormField(
                controller: _breederController,
                decoration: InputDecoration(
                  labelText: 'Breeder',
                  labelStyle: const TextStyle(color: Colors.white),
                  prefixIcon: const Icon(Icons.business, color: Colors.white),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: AppColors.primary500),
                  ),
                  filled: true,
                  fillColor: const Color(0xFF2a2a2a),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              // Genetics Section
              const SizedBox(height: 24),
              _buildSectionHeader('Genetics'),
              const SizedBox(height: 16),

              GeneticsSlider(
                indicaPercentage: _indicaPercentage,
                sativaPercentage: _sativaPercentage,
                onIndicaChanged: (value) {
                  setState(() {
                    _indicaPercentage = value;
                    _sativaPercentage = 100 - value;
                  });
                },
                onSativaChanged: (value) {
                  setState(() {
                    _sativaPercentage = value;
                    _indicaPercentage = 100 - value;
                  });
                },
              ),

              const SizedBox(height: 16),

              // Autoflower toggle
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: const Color(0xFF2a2a2a),
                  borderRadius: BorderRadius.circular(8),
                  border: Border.all(color: Colors.white12),
                ),
                child: SwitchListTile(
                  title: const Text(
                    'Autoflowering',
                    style: TextStyle(color: Colors.white),
                  ),
                  subtitle: const Text(
                    'Automatically flowers after a certain age',
                    style: TextStyle(color: Colors.white70, fontSize: 12),
                  ),
                  value: _autoflower,
                  onChanged: (value) {
                    setState(() {
                      _autoflower = value;
                    });
                  },
                  activeThumbColor: AppColors.primary500,
                ),
              ),

              // Cultivation Details
              const SizedBox(height: 24),
              _buildSectionHeader('Cultivation Details'),
              const SizedBox(height: 16),

              TextFormField(
                controller: _floweringTimeController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'Flowering Time (days)',
                  labelStyle: const TextStyle(color: Colors.white),
                  prefixIcon: const Icon(Icons.timer, color: Colors.white),
                  suffixText: 'days',
                  suffixStyle: const TextStyle(color: Colors.white70),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: AppColors.primary500),
                  ),
                  filled: true,
                  fillColor: const Color(0xFF2a2a2a),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              // Description
              const SizedBox(height: 24),
              _buildSectionHeader('Description'),
              const SizedBox(height: 16),

              TextFormField(
                controller: _descriptionController,
                maxLines: 4,
                decoration: InputDecoration(
                  labelText: 'Description',
                  labelStyle: const TextStyle(color: Colors.white),
                  hintText:
                      'Detailed information about effects, taste, growing notes, etc.',
                  hintStyle: const TextStyle(color: Colors.white38),
                  prefixIcon: const Icon(
                    Icons.description,
                    color: Colors.white,
                  ),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: AppColors.primary500),
                  ),
                  filled: true,
                  fillColor: const Color(0xFF2a2a2a),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              const SizedBox(height: 16),

              TextFormField(
                controller: _referenceUrlController,
                decoration: InputDecoration(
                  labelText: 'Reference URL',
                  labelStyle: const TextStyle(color: Colors.white),
                  hintText: 'https://example.com/strain-info',
                  hintStyle: const TextStyle(color: Colors.white38),
                  prefixIcon: const Icon(Icons.link, color: Colors.white),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  enabledBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: Colors.white24),
                  ),
                  focusedBorder: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                    borderSide: const BorderSide(color: AppColors.primary500),
                  ),
                  filled: true,
                  fillColor: const Color(0xFF2a2a2a),
                ),
                style: const TextStyle(color: Colors.white),
              ),

              const SizedBox(height: 32),

              // Submit button
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: _isLoading ? null : _handleCreateStrain,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: AppColors.primary500,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8),
                    ),
                  ),
                  child: _isLoading
                      ? const SizedBox(
                          height: 20,
                          width: 20,
                          child: CircularProgressIndicator(
                            valueColor: AlwaysStoppedAnimation<Color>(
                              Colors.white,
                            ),
                            strokeWidth: 2,
                          ),
                        )
                      : const Text(
                          'Create Strain',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                ),
              ),

              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Text(
      title,
      style: const TextStyle(
        fontSize: 18,
        fontWeight: FontWeight.bold,
        color: AppColors.primary500,
      ),
    );
  }
}
