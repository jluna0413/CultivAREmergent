import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import '../../../core/providers/riverpod_exports.dart';
import 'package:go_router/go_router.dart';
import '../domain/plant_model.dart';
import '../../../core/widgets/glass_card.dart';

class PlantCard extends ConsumerWidget {
  const PlantCard({
    super.key,
    required this.plant,
    this.onTap,
    this.onEdit,
    this.onDelete,
    this.onWater,
    this.onFeed,
    this.compact = false,
    this.showProgress = false,
  });

  final Plant plant;
  final VoidCallback? onTap;
  final VoidCallback? onEdit;
  final VoidCallback? onDelete;
  final VoidCallback? onWater;
  final VoidCallback? onFeed;
  final bool compact;
  final bool showProgress;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final textTheme = Theme.of(context).textTheme;

    final cardContent = LayoutBuilder(
      builder: (context, constraints) {
        final isCompact = compact || constraints.maxWidth < 600;

        if (isCompact) {
          return buildCompactLayout(context, textTheme);
        } else {
          return buildFullLayout(context, textTheme);
        }
      },
    );

    return Semantics(
      label: '${plant.name} - ${_statusLabel(plant)}',
      child: GlassCard(
        child: InkWell(
          key: const ValueKey('plant_card_inkwell'),
          onTap: onTap ?? () => context.go('/plants/${plant.id}'),
          child: cardContent,
        ),
      ),
    );
  }

  Widget buildCompactLayout(BuildContext context, TextTheme textTheme) {
    return Row(
      children: [
        buildImage(height: 80, width: 80),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                plant.name,
                style: textTheme.titleMedium,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 4),
              Expanded(
                child: Row(
                  children: [
                    const Icon(
                      Icons.biotech,
                      size: 16,
                    ), // Using Icons.biotech for DNA
                    const SizedBox(width: 4),
                    Expanded(
                      child: Text(
                        _strainLabel(plant),
                        style: textTheme.bodySmall,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        if (onEdit != null || onDelete != null)
          Row(
            children: [
              if (onEdit != null)
                IconButton(icon: const Icon(Icons.edit), onPressed: onEdit),
              if (onDelete != null)
                IconButton(icon: const Icon(Icons.delete), onPressed: onDelete),
            ],
          ),
      ],
    );
  }

  Widget buildFullLayout(BuildContext context, TextTheme textTheme) {
    final strainLabel = _strainLabel(plant);
    final ageInDays = _ageInDays(plant);
    final progress = _growthProgress(plant);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        buildImage(height: 150),
        Padding(
          padding: const EdgeInsets.all(12.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                plant.name,
                style: textTheme.headlineSmall,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(
                    Icons.biotech,
                    size: 18,
                  ), // Using Icons.biotech for DNA
                  const SizedBox(width: 8),
                  Text(strainLabel, style: textTheme.titleMedium),
                ],
              ),
              const SizedBox(height: 8),
              Row(
                children: [
                  const Icon(Icons.calendar_today, size: 16),
                  const SizedBox(width: 8),
                  Text('$ageInDays days', style: textTheme.bodyMedium),
                  const SizedBox(width: 16),
                  const Icon(Icons.location_on, size: 16),
                  const SizedBox(width: 8),
                  Text(
                    plant.description ?? 'No description',
                    style: textTheme.bodyMedium,
                  ),
                ],
              ),
              if (showProgress && progress != null) ...[
                const SizedBox(height: 8),
                LinearProgressIndicator(value: progress),
              ],
            ],
          ),
        ),
        const Spacer(),
        buildActionButtons(context),
      ],
    );
  }

  Widget buildImage({required double height, double? width}) {
    final statusLabel = _statusLabel(plant);
    final statusColor = _statusColor(plant);
    return Hero(
      tag: 'plant_image_${plant.id}',
      child: Stack(
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.only(
              topLeft: Radius.circular(20),
              topRight: Radius.circular(20),
            ),
            child: CachedNetworkImage(
              imageUrl: plant.imageUrl ?? '',
              height: height,
              width: width ?? double.infinity,
              fit: BoxFit.cover,
              placeholder: (context, url) =>
                  const Center(child: Icon(Icons.grass)),
              errorWidget: (context, url, error) =>
                  const Center(child: Icon(Icons.error)),
            ),
          ),
          Positioned(
            top: 8,
            right: 8,
            child: Chip(
              label: Text(statusLabel),
              backgroundColor: statusColor,
              labelStyle: const TextStyle(color: Colors.white),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildActionButtons(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          if (onEdit != null)
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: onEdit,
              tooltip: 'Edit',
            ),
          if (onDelete != null)
            IconButton(
              icon: const Icon(Icons.delete, color: Colors.redAccent),
              onPressed: () {
                // It's good practice to show a confirmation dialog before deleting
                showDialog(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: const Text('Confirm Delete'),
                      content: Text(
                        'Are you sure you want to delete ${plant.name}?',
                      ),
                      actions: <Widget>[
                        TextButton(
                          child: const Text('Cancel'),
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                        ),
                        TextButton(
                          style: TextButton.styleFrom(
                            foregroundColor: Colors.red,
                          ),
                          child: const Text('Delete'),
                          onPressed: () {
                            Navigator.of(context).pop();
                            onDelete!();
                          },
                        ),
                      ],
                    );
                  },
                );
              },
              tooltip: 'Delete',
            ),
          if (onWater != null)
            IconButton(
              icon: const Icon(Icons.water_drop, color: Colors.blue),
              onPressed: onWater,
              tooltip: 'Water',
            ),
          if (onFeed != null)
            IconButton(
              icon: const Icon(Icons.local_florist, color: Colors.brown),
              onPressed: onFeed,
              tooltip: 'Feed',
            ),
        ],
      ),
    );
  }

  String _statusLabel(Plant plant) {
    // Use the statusName computed property
    return plant.statusName ?? 'Unknown';
  }

  Color _statusColor(Plant plant) {
    final status = (plant.statusName ?? '').toLowerCase();
    switch (status) {
      case 'seedling':
        return Colors.lightGreen;
      case 'vegetative':
        return Colors.green;
      case 'flowering':
        return Colors.yellow;
      case 'harvest':
        return Colors.orange;
      case 'curing':
        return Colors.brown;
      default:
        return Colors.grey;
    }
  }

  String _strainLabel(Plant plant) {
    // Use description as strain info since there's no strain field
    return plant.description ?? 'Unknown';
  }

  int _ageInDays(Plant plant) {
    final start = plant.startDt;
    if (start == null) {
      return 0;
    }
    return DateTime.now().difference(start).inDays;
  }

  double? _growthProgress(Plant plant) {
    final start = plant.startDt;
    final harvest = plant.harvestDate;
    if (start == null || harvest == null) {
      return null;
    }
    final totalDays = harvest.difference(start).inDays;
    if (totalDays <= 0) {
      return null;
    }
    final elapsed = plant.currentDay ?? DateTime.now().difference(start).inDays;
    return (elapsed / totalDays).clamp(0, 1);
  }
}
