import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../domain/plant_model.dart';
import '../providers/plants_providers.dart';
import '../../../core/widgets/error_view.dart';
import '../../../core/widgets/glass_card.dart';
import '../../journal/widgets/sbt_badge_widget.dart';

final plantDetailProvider = FutureProvider.autoDispose.family<Plant, int>((
  ref,
  id,
) async {
  // This is not efficient, but it's a temporary solution
  // until a proper single plant endpoint is available.
  final plants = await ref.watch(plantsApiClientProvider).getPlants();
  return plants.items.firstWhere((element) => element.id == id);
});

class PlantDetailScreen extends ConsumerWidget {
  const PlantDetailScreen({super.key, required this.plantId});
  final int plantId;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final plantAsync = ref.watch(plantDetailProvider(plantId));

    return Scaffold(
      appBar: AppBar(
        title: plantAsync.when(
          data: (plant) => Text(plant.name),
          loading: () => const Text('Loading...'),
          error: (error, stack) => const Text('Error'),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.edit),
            onPressed: () => context.go('/plants/$plantId/edit'),
          ),
          Consumer(
            builder: (context, ref, child) {
              final isLoading = ref.watch(deletePlantLoadingProvider(plantId));
              final error = ref.watch(deletePlantErrorProvider(plantId));
              final success = ref.watch(deletePlantSuccessProvider(plantId));

              return IconButton(
                icon: isLoading
                    ? const SizedBox(
                        width: 20,
                        height: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.delete),
                onPressed: isLoading
                    ? null
                    : () async {
                        await ref.read(deletePlantProvider(plantId).future);
                        if (success && context.mounted) {
                          context.pop();
                        }
                      },
              );
            },
          ),
        ],
      ),
      body: plantAsync.when(
        data: (plant) => SingleChildScrollView(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Center(
                child: Hero(
                  tag: 'plant-image-$plantId',
                  child: Stack(
                    alignment: Alignment.bottomRight,
                    children: [
                      CircleAvatar(
                        radius: 60,
                        backgroundImage: plant.imageUrl != null
                            ? NetworkImage(plant.imageUrl!)
                            : null,
                        child: plant.imageUrl == null
                            ? const Icon(Icons.local_florist, size: 60)
                            : null,
                      ),
                      // Mock SBT Badge Injection (Ideally fetched from backend)
                      const Positioned(
                        right: 0,
                        bottom: 0,
                        child: SBTBadgeWidget(type: SBTType.masterGrower),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
              GlassCard(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'ID: ${plant.id}',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Text(
                        'Status: ${plant.statusName}',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      Text(
                        'Day: ${plant.currentDay ?? 0}',
                        style: const TextStyle(color: Colors.white70),
                      ),
                      if (plant.description != null)
                        Text(
                          'Description: ${plant.description!}',
                          style: const TextStyle(color: Colors.white70),
                        ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => ErrorView(message: error.toString()),
      ),
    );
  }
}
