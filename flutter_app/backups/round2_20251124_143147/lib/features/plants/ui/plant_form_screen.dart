import 'package:flutter/material.dart';
import '../../core/providers/riverpod_exports.dart';
import '../../features/plants/domain/plant_model.dart';
import '../../features/plants/providers/plants_providers.dart';
import 'package:flutter_form_builder/flutter_form_builder.dart';
import 'package:form_builder_validators/form_builder_validators.dart';
import 'package:image_picker/image_picker.dart';

class PlantFormScreen extends ConsumerWidget {
  const PlantFormScreen({super.key, this.plant});
  final Plant? plant;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final formKey = GlobalKey<FormBuilderState>();

    return Scaffold(
      appBar: AppBar(
        title: Text(plant == null ? 'Create Plant' : 'Edit Plant'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: FormBuilder(
          key: formKey,
          child: SingleChildScrollView(
            child: Column(
              children: [
                FormBuilderTextField(
                  name: 'name',
                  initialValue: plant?.name,
                  decoration: const InputDecoration(labelText: 'Name'),
                  validator: FormBuilderValidators.required(),
                ),
                FormBuilderTextField(
                  name: 'description',
                  initialValue: plant?.description,
                  decoration: const InputDecoration(labelText: 'Description'),
                ),
                FormBuilderDropdown(
                  name: 'statusId',
                  initialValue: plant?.statusId,
                  decoration: const InputDecoration(labelText: 'Status'),
                  items: const [
                    DropdownMenuItem(value: 1, child: Text('Seedling')),
                    DropdownMenuItem(value: 2, child: Text('Vegetative')),
                    DropdownMenuItem(value: 3, child: Text('Flowering')),
                    DropdownMenuItem(value: 4, child: Text('Harvested')),
                  ],
                  validator: FormBuilderValidators.required(),
                ),
                FormBuilderDateTimePicker(
                  name: 'startDt',
                  initialValue: plant?.startDt,
                  decoration: const InputDecoration(labelText: 'Start Date'),
                ),
                FormBuilderCheckbox(
                  name: 'isClone',
                  initialValue: plant?.isClone ?? false,
                  title: const Text('Is Clone'),
                ),
                FormBuilderCheckbox(
                  name: 'autoflower',
                  initialValue: plant?.autoflower ?? false,
                  title: const Text('Autoflower'),
                ),
                // Image picker logic would go here
                ElevatedButton(
                  onPressed: () async {
                    if (formKey.currentState?.saveAndValidate() ?? false) {
                      final formData = formKey.currentState!.value;
                      if (plant == null) {
                        final newPlant = PlantCreate(
                          name: formData['name'],
                          description: formData['description'],
                          statusId: formData['statusId'],
                          startDt: formData['startDt'],
                          isClone: formData['isClone'],
                          autoflower: formData['autoflower'],
                        );
                        // Call provider to create plant
                        await ref
                            .read(plantsApiClientProvider)
                            .createPlant(newPlant);
                      } else {
                        final updatedPlant = PlantUpdate(
                          name: formData['name'],
                          description: formData['description'],
                          statusId: formData['statusId'],
                          startDt: formData['startDt'],
                          isClone: formData['isClone'],
                          autoflower: formData['autoflower'],
                        );
                        // Call provider to update plant
                        await ref
                            .read(plantsApiClientProvider)
                            .updatePlant(plant!.id, updatedPlant);
                      }
                      ref.invalidate(plantsListProvider);
                      Navigator.of(context).pop();
                    }
                  },
                  child: const Text('Submit'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
