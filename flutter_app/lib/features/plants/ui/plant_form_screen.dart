import 'package:flutter/material.dart';
import '../../../core/providers/riverpod_exports.dart';
import '../../../core/providers/cultivar_provider.dart';
import '../../../core/providers/zones_provider.dart';
import '../domain/plant_model.dart';
import '../providers/plants_providers.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:form_builder_validators/form_builder_validators.dart';

class PlantFormScreen extends ConsumerStatefulWidget {
  const PlantFormScreen({super.key, this.plant});
  final Plant? plant;

  @override
  ConsumerState<PlantFormScreen> createState() => _PlantFormScreenState();
}

class _PlantFormScreenState extends ConsumerState<PlantFormScreen> {
  final formKey = GlobalKey<FormBuilderState>();
  PlantCreate? _pendingCreateData;
  bool _isClone = false;

  @override
  void initState() {
    super.initState();
    _isClone = widget.plant?.isClone ?? false;
  }

  @override
  Widget build(BuildContext context) {
    final cultivarsState = ref.watch(cultivarsProvider);
    final zonesState = ref.watch(zonesProvider);

    return Dialog(
      insetPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 24),
      child: Container(
        constraints: const BoxConstraints(maxWidth: 600, maxHeight: 800),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            // Modal Header
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor,
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(8),
                  topRight: Radius.circular(8),
                ),
              ),
              child: Row(
                children: [
                  Icon(
                    widget.plant == null ? Icons.add_circle : Icons.edit,
                    color: Colors.white,
                    size: 28,
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      widget.plant == null ? 'Add New Plant' : 'Edit Plant',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  IconButton(
                    onPressed: () => Navigator.of(context).pop(),
                    icon: const Icon(Icons.close, color: Colors.white),
                    tooltip: 'Close',
                  ),
                ],
              ),
            ),

            // Modal Body
            Flexible(
              child: Container(
                color: Colors.white,
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24),
                  child: FormBuilder(
                    key: formKey,
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Plant Information Card
                        _buildFormCard('Plant Information', Icons.local_florist, [
                          // Plant Name
                          FormBuilderTextField(
                            name: 'name',
                            initialValue: widget.plant?.name,
                            decoration: InputDecoration(
                              labelText: 'Plant Name *',
                              hintText: 'e.g., Northern Lights #1',
                              prefixIcon: const Icon(Icons.label),
                              border: const OutlineInputBorder(),
                              filled: true,
                              fillColor: Colors.grey.shade50,
                            ),
                            validator: FormBuilderValidators.compose([
                              FormBuilderValidators.required(),
                              FormBuilderValidators.minLength(2),
                              FormBuilderValidators.maxLength(100),
                            ]),
                          ),
                          const SizedBox(height: 16),

                          // Strain Selection
                          cultivarsState.when(
                            data: (cultivarsData) {
                              final cultivars = cultivarsData.filteredCultivars;
                              return FormBuilderDropdown<String>(
                                name: 'cultivarId',
                                initialValue: widget.plant?.cultivarId
                                    ?.toString(),
                                decoration: InputDecoration(
                                  labelText: 'Strain *',
                                  prefixIcon: const Icon(Icons.grass),
                                  border: const OutlineInputBorder(),
                                  filled: true,
                                  fillColor: Colors.grey.shade50,
                                  helperText: 'Select the cannabis strain',
                                ),
                                items: cultivars.map((cultivar) {
                                  return DropdownMenuItem<String>(
                                    value: cultivar.id.toString(),
                                    child: Row(
                                      children: [
                                        Container(
                                          width: 12,
                                          height: 12,
                                          decoration: BoxDecoration(
                                            color: _getStrainColor(
                                              cultivar.type,
                                            ),
                                            shape: BoxShape.circle,
                                          ),
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          child: Text(
                                            cultivar.name,
                                            overflow: TextOverflow.ellipsis,
                                          ),
                                        ),
                                        if (cultivar.thcLevel > 0)
                                          Text(
                                            ' ${cultivar.thcLevel.toStringAsFixed(1)}% THC',
                                            style: TextStyle(
                                              fontSize: 12,
                                              color: Colors.grey.shade600,
                                            ),
                                          ),
                                      ],
                                    ),
                                  );
                                }).toList(),
                                validator: FormBuilderValidators.required(),
                              );
                            },
                            loading: () => const CircularProgressIndicator(),
                            error: (error, _) =>
                                Text('Error loading strains: $error'),
                          ),
                          const SizedBox(height: 16),

                          // Zone Selection
                          zonesState.when(
                            data: (zonesData) {
                              final zones = zonesData.activeZones;
                              return FormBuilderDropdown<String>(
                                name: 'zoneId',
                                initialValue: widget.plant?.zoneId?.toString(),
                                decoration: InputDecoration(
                                  labelText: 'Zone *',
                                  prefixIcon: const Icon(Icons.location_on),
                                  border: const OutlineInputBorder(),
                                  filled: true,
                                  fillColor: Colors.grey.shade50,
                                  helperText: 'Select the grow location',
                                ),
                                items: zones.map((zone) {
                                  final available =
                                      zone.capacity == null ||
                                      zone.currentPlants < zone.capacity!;
                                  return DropdownMenuItem<String>(
                                    value: zone.id,
                                    child: Row(
                                      children: [
                                        Icon(
                                          _getZoneIcon(zone.id),
                                          size: 16,
                                          color: available
                                              ? Colors.green
                                              : Colors.orange,
                                        ),
                                        const SizedBox(width: 8),
                                        Expanded(
                                          child: Column(
                                            crossAxisAlignment:
                                                CrossAxisAlignment.start,
                                            children: [
                                              Text(zone.name),
                                              if (zone.capacity != null)
                                                Text(
                                                  '${zone.currentPlants}/${zone.capacity} plants',
                                                  style: TextStyle(
                                                    fontSize: 12,
                                                    color: available
                                                        ? Colors.green
                                                        : Colors.orange,
                                                  ),
                                                ),
                                            ],
                                          ),
                                        ),
                                      ],
                                    ),
                                  );
                                }).toList(),
                                validator: FormBuilderValidators.required(),
                              );
                            },
                            loading: () => const CircularProgressIndicator(),
                            error: (error, _) =>
                                Text('Error loading zones: $error'),
                          ),
                        ]),

                        const SizedBox(height: 24),

                        // Growth Information Card
                        _buildFormCard('Growth Information', Icons.timeline, [
                          // Status Selection
                          FormBuilderDropdown<int>(
                            name: 'statusId',
                            initialValue: widget.plant?.statusId ?? 1,
                            decoration: InputDecoration(
                              labelText: 'Growth Stage *',
                              prefixIcon: const Icon(Icons.trending_up),
                              border: const OutlineInputBorder(),
                              filled: true,
                              fillColor: Colors.grey.shade50,
                              helperText: 'Current stage of plant growth',
                            ),
                            items: const [
                              DropdownMenuItem(
                                value: 1,
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.spa,
                                      color: Colors.green,
                                      size: 16,
                                    ),
                                    SizedBox(width: 8),
                                    Text('Seedling'),
                                  ],
                                ),
                              ),
                              DropdownMenuItem(
                                value: 2,
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.grass,
                                      color: Colors.blue,
                                      size: 16,
                                    ),
                                    SizedBox(width: 8),
                                    Text('Vegetative'),
                                  ],
                                ),
                              ),
                              DropdownMenuItem(
                                value: 3,
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.local_florist,
                                      color: Colors.purple,
                                      size: 16,
                                    ),
                                    SizedBox(width: 8),
                                    Text('Flowering'),
                                  ],
                                ),
                              ),
                              DropdownMenuItem(
                                value: 4,
                                child: Row(
                                  children: [
                                    Icon(
                                      Icons.inventory,
                                      color: Colors.brown,
                                      size: 16,
                                    ),
                                    SizedBox(width: 8),
                                    Text('Harvested'),
                                  ],
                                ),
                              ),
                            ],
                            validator: FormBuilderValidators.required(),
                          ),
                          const SizedBox(height: 16),

                          // Start Date
                          FormBuilderDateTimePicker(
                            name: 'startDt',
                            initialValue:
                                widget.plant?.startDt ?? DateTime.now(),
                            inputType: InputType.date,
                            decoration: InputDecoration(
                              labelText: 'Start Date *',
                              prefixIcon: const Icon(Icons.calendar_today),
                              border: const OutlineInputBorder(),
                              filled: true,
                              fillColor: Colors.grey.shade50,
                              helperText:
                                  'When did you start growing this plant?',
                            ),
                            validator: FormBuilderValidators.compose([
                              FormBuilderValidators.required(),
                              (value) {
                                if (value != null &&
                                    value.isAfter(DateTime.now())) {
                                  return 'Start date cannot be in the future';
                                }
                                return null;
                              },
                            ]),
                          ),
                        ]),

                        const SizedBox(height: 24),

                        // Clone Information Card
                        _buildFormCard('Clone Information', Icons.call_split, [
                          // Is Clone Checkbox
                          FormBuilderCheckbox(
                            name: 'isClone',
                            initialValue: _isClone,
                            title: const Row(
                              children: [
                                Icon(Icons.call_split, size: 16),
                                SizedBox(width: 8),
                                Text('This is a clone'),
                              ],
                            ),
                            onChanged: (value) {
                              setState(() => _isClone = value ?? false);
                            },
                          ),

                          // Parent Plant Selection (conditional)
                          if (_isClone) ...[
                            const SizedBox(height: 16),
                            // TODO: Load actual plants for parent selection
                            FormBuilderDropdown<String>(
                              name: 'parentId',
                              decoration: InputDecoration(
                                labelText: 'Parent Plant',
                                prefixIcon: const Icon(Icons.family_restroom),
                                border: const OutlineInputBorder(),
                                filled: true,
                                fillColor: Colors.grey.shade50,
                                helperText:
                                    'Select the plant this clone came from',
                              ),
                              items: const [
                                // TODO: Load from plants provider
                                DropdownMenuItem(
                                  value: '1',
                                  child: Text('Northern Lights #1 (Mother)'),
                                ),
                                DropdownMenuItem(
                                  value: '2',
                                  child: Text('Blue Dream #1 (Mother)'),
                                ),
                              ],
                            ),
                          ],
                        ]),

                        const SizedBox(height: 24),

                        // Notes Card
                        _buildFormCard('Additional Notes', Icons.note, [
                          FormBuilderTextField(
                            name: 'description',
                            initialValue: widget.plant?.description,
                            maxLines: 4,
                            decoration: InputDecoration(
                              labelText: 'Notes',
                              hintText:
                                  'Any additional notes about this plant...',
                              prefixIcon: const Icon(Icons.note),
                              border: const OutlineInputBorder(),
                              filled: true,
                              fillColor: Colors.grey.shade50,
                            ),
                            validator: FormBuilderValidators.maxLength(500),
                          ),
                        ]),

                        const SizedBox(height: 32),

                        // Action Buttons
                        if (widget.plant == null) ...[
                          // Create plant
                          Builder(
                            builder: (context) {
                              final isLoading = _pendingCreateData != null
                                  ? ref.watch(
                                      createPlantLoadingProvider(
                                        _pendingCreateData!,
                                      ),
                                    )
                                  : false;
                              final error = _pendingCreateData != null
                                  ? ref.watch(
                                      createPlantErrorProvider(
                                        _pendingCreateData!,
                                      ),
                                    )
                                  : null;

                              return Column(
                                children: [
                                  if (error != null)
                                    Container(
                                      padding: const EdgeInsets.all(16),
                                      margin: const EdgeInsets.only(bottom: 16),
                                      decoration: BoxDecoration(
                                        color: Colors.red.shade50,
                                        borderRadius: BorderRadius.circular(8),
                                        border: Border.all(
                                          color: Colors.red.shade200,
                                        ),
                                      ),
                                      child: Row(
                                        children: [
                                          const Icon(
                                            Icons.error,
                                            color: Colors.red,
                                          ),
                                          const SizedBox(width: 12),
                                          Expanded(
                                            child: Text(
                                              'Error: $error',
                                              style: const TextStyle(
                                                color: Colors.red,
                                              ),
                                            ),
                                          ),
                                        ],
                                      ),
                                    ),

                                  Row(
                                    children: [
                                      Expanded(
                                        child: OutlinedButton(
                                          onPressed: isLoading
                                              ? null
                                              : () {
                                                  formKey.currentState?.reset();
                                                  setState(
                                                    () => _isClone = false,
                                                  );
                                                },
                                          style: OutlinedButton.styleFrom(
                                            padding: const EdgeInsets.symmetric(
                                              vertical: 16,
                                            ),
                                          ),
                                          child: const Text('Reset Form'),
                                        ),
                                      ),
                                      const SizedBox(width: 16),
                                      Expanded(
                                        child: ElevatedButton(
                                          onPressed: isLoading
                                              ? null
                                              : () async {
                                                  if (formKey.currentState
                                                          ?.saveAndValidate() ??
                                                      false) {
                                                    final formData = formKey
                                                        .currentState!
                                                        .value;

                                                    final newPlant = PlantCreate(
                                                      name:
                                                          formData['name']
                                                              as String,
                                                      description:
                                                          formData['description']
                                                              as String?,
                                                      statusId:
                                                          formData['statusId']
                                                              as int,
                                                      cultivarId: int.tryParse(
                                                        formData['cultivarId']
                                                            as String,
                                                      ),
                                                      zoneId:
                                                          _getZoneIdFromString(
                                                            formData['zoneId']
                                                                as String,
                                                          ),
                                                      isClone:
                                                          formData['isClone']
                                                              as bool? ??
                                                          false,
                                                      parentId:
                                                          formData['parentId'] !=
                                                              null
                                                          ? int.tryParse(
                                                              formData['parentId']
                                                                  as String,
                                                            )
                                                          : null,
                                                      autoflower:
                                                          false, // TODO: Determine from cultivar
                                                    );

                                                    setState(
                                                      () => _pendingCreateData =
                                                          newPlant,
                                                    );

                                                    try {
                                                      await ref.read(
                                                        createPlantProvider(
                                                          newPlant,
                                                        ).future,
                                                      );
                                                      final successPlant = ref.read(
                                                        createPlantSuccessProvider(
                                                          newPlant,
                                                        ),
                                                      );
                                                      if (successPlant !=
                                                              null &&
                                                          context.mounted) {
                                                        Navigator.of(
                                                          context,
                                                        ).pop(successPlant);
                                                      }
                                                    } finally {
                                                      if (mounted) {
                                                        setState(
                                                          () =>
                                                              _pendingCreateData =
                                                                  null,
                                                        );
                                                      }
                                                    }
                                                  }
                                                },
                                          style: ElevatedButton.styleFrom(
                                            padding: const EdgeInsets.symmetric(
                                              vertical: 16,
                                            ),
                                          ),
                                          child: isLoading
                                              ? const SizedBox(
                                                  width: 20,
                                                  height: 20,
                                                  child:
                                                      CircularProgressIndicator(
                                                        strokeWidth: 2,
                                                      ),
                                                )
                                              : const Row(
                                                  mainAxisAlignment:
                                                      MainAxisAlignment.center,
                                                  children: [
                                                    Icon(Icons.save),
                                                    SizedBox(width: 8),
                                                    Text('Save Plant'),
                                                  ],
                                                ),
                                        ),
                                      ),
                                    ],
                                  ),
                                ],
                              );
                            },
                          ),
                        ] else ...[
                          // Update plant - placeholder for now
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton(
                              onPressed: () {
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(
                                    content: Text(
                                      'Update functionality coming soon!',
                                    ),
                                  ),
                                );
                              },
                              style: ElevatedButton.styleFrom(
                                padding: const EdgeInsets.symmetric(
                                  vertical: 16,
                                ),
                              ),
                              child: const Row(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  Icon(Icons.update),
                                  SizedBox(width: 8),
                                  Text('Update Plant'),
                                ],
                              ),
                            ),
                          ),
                        ],
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFormCard(String title, IconData icon, List<Widget> children) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: Theme.of(context).primaryColor),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            ...children,
          ],
        ),
      ),
    );
  }

  Color _getStrainColor(CultivarType? type) {
    switch (type) {
      case CultivarType.indica:
        return Colors.purple;
      case CultivarType.sativa:
        return Colors.orange;
      case CultivarType.hybrid:
        return Colors.green;
      case CultivarType.ruderalis:
        return Colors.blue;
      default:
        return Colors.grey;
    }
  }

  IconData _getZoneIcon(String zoneId) {
    switch (zoneId) {
      case 'indoor':
        return Icons.home;
      case 'outdoor':
        return Icons.park;
      case 'greenhouse':
        return Icons.agriculture;
      case 'tent':
        return Icons.store;
      default:
        return Icons.location_on;
    }
  }

  int? _getZoneIdFromString(String zoneId) {
    // Map zone string IDs to integer IDs for backend
    // This is a temporary mapping - in production, zones would have proper integer IDs
    switch (zoneId) {
      case 'indoor':
        return 1;
      case 'outdoor':
        return 2;
      case 'greenhouse':
        return 3;
      case 'tent':
        return 4;
      default:
        return null;
    }
  }
}
