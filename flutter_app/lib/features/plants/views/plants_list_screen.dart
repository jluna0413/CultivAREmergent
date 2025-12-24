import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../domain/plant_model.dart';
import '../widgets/plant_card.dart';

class PlantsListScreen extends ConsumerWidget {
  const PlantsListScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // Mock data for demonstration
    // Use domain Plant model fields: statusId (int) and optional statusName
    final plants = [
      Plant(
        id: 1,
        userId: 1,
        name: 'Big Bud',
        statusId: 3, // flowering
        statusName: 'flowering',
        description: 'Indica',
        startDt: DateTime.now().subtract(const Duration(days: 45)),
        imageUrl: 'https://via.placeholder.com/300/4CAF50/FFFFFF?text=Plant+1',
      ),
      Plant(
        id: 2,
        userId: 1,
        name: 'Sour Diesel',
        statusId: 2, // vegetative
        statusName: 'vegetative',
        description: 'Sativa',
        startDt: DateTime.now().subtract(const Duration(days: 20)),
        imageUrl: 'https://via.placeholder.com/300/2196F3/FFFFFF?text=Plant+2',
      ),
      Plant(
        id: 3,
        userId: 1,
        name: 'OG Kush',
        statusId: 1, // seedling
        statusName: 'seedling',
        description: 'Hybrid',
        startDt: DateTime.now().subtract(const Duration(days: 5)),
        imageUrl: 'https://via.placeholder.com/300/FFC107/FFFFFF?text=Plant+3',
      ),
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('My Plants')),
      body: GridView.builder(
        padding: const EdgeInsets.all(8.0),
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 8.0,
          mainAxisSpacing: 8.0,
          childAspectRatio: 0.75,
        ),
        itemCount: plants.length,
        itemBuilder: (context, index) {
          final plant = plants[index];
          return PlantCard(
                plant: plant,
                onEdit: () {},
                onDelete: () {},
                onWater: () {},
                onFeed: () {},
              )
              as Widget;
        },
      ),
    );
  }
}
