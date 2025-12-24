import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../domain/plant_model.dart';
import '../providers/plants_providers.dart';
import '../../../core/widgets/error_view.dart';
import '../../../core/widgets/glass_card.dart';

class PlantsListScreen extends ConsumerStatefulWidget {
  const PlantsListScreen({super.key});

  @override
  ConsumerState<PlantsListScreen> createState() => _PlantsListScreenState();
}

class _PlantsListScreenState extends ConsumerState<PlantsListScreen> {
  final _searchController = TextEditingController();
  String _statusFilter = 'all';

  @override
  Widget build(BuildContext context) {
    final plantsAsync = ref.watch(
      plantsListProvider(
        PlantsParams(search: _searchController.text, status: _statusFilter),
      ),
    );

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Plants'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => context.go('/plants/new'),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: TextField(
              controller: _searchController,
              decoration: InputDecoration(
                hintText: 'Search Plants...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: IconButton(
                  icon: const Icon(Icons.clear),
                  onPressed: () {
                    _searchController.clear();
                    setState(() {});
                  },
                ),
              ),
              onChanged: (value) => setState(() {}),
            ),
          ),
          Wrap(
            spacing: 8.0,
            children: [
              FilterChip(
                label: const Text('All'),
                selected: _statusFilter == 'all',
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _statusFilter = 'all');
                  }
                },
              ),
              FilterChip(
                label: const Text('Seedling'),
                selected: _statusFilter == 'seedling',
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _statusFilter = 'seedling');
                  }
                },
              ),
              FilterChip(
                label: const Text('Vegetative'),
                selected: _statusFilter == 'vegetative',
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _statusFilter = 'vegetative');
                  }
                },
              ),
              FilterChip(
                label: const Text('Flowering'),
                selected: _statusFilter == 'flowering',
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _statusFilter = 'flowering');
                  }
                },
              ),
              FilterChip(
                label: const Text('Harvested'),
                selected: _statusFilter == 'harvested',
                onSelected: (selected) {
                  if (selected) {
                    setState(() => _statusFilter = 'harvested');
                  }
                },
              ),
            ],
          ),
          Expanded(
            child: plantsAsync.when(
              data: (data) => ListView.builder(
                itemCount: data.items.length,
                itemBuilder: (context, index) {
                  final plant = data.items[index];
                  return GestureDetector(
                    onTap: () => context.go('/plants/${plant.id}'),
                    child: GlassCard(
                      child: ListTile(
                        leading: plant.imageUrl != null
                            ? Image.network(plant.imageUrl!)
                            : const Icon(Icons.local_florist),
                        title: Text(plant.name),
                        subtitle: Text(plant.statusName ?? 'Unknown'),
                        trailing: Text('Day ${plant.currentDay ?? 0}'),
                      ),
                    ),
                  );
                },
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (error, stack) => ErrorView(message: error.toString()),
            ),
          ),
        ],
      ),
    );
  }
}
