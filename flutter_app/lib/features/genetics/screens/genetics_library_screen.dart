import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/theme/app_theme.dart';
import '../providers/genetics_provider.dart';
import '../widgets/strain_card.dart';

class GeneticsLibraryScreen extends ConsumerWidget {
  const GeneticsLibraryScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final geneticsAsync = ref.watch(geneticsLibraryProvider);

    return Scaffold(
      backgroundColor: AppTheme.getBackgroundColor(context),
      body: CustomScrollView(
        slivers: [
          // Apple-Style Large Title App Bar
          SliverAppBar.large(
            title: const Text("Genetics Library"),
            backgroundColor: AppTheme.getBackgroundColor(context),
            surfaceTintColor: Colors.transparent,
            actions: [
              IconButton(icon: const Icon(Icons.search), onPressed: () {}),
              IconButton(icon: const Icon(Icons.filter_list), onPressed: () {}),
            ],
          ),

          // Content
          geneticsAsync.when(
            data: (strains) => SliverPadding(
              padding: const EdgeInsets.all(16),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithMaxCrossAxisExtent(
                  maxCrossAxisExtent: 220, // Responsive Card Width
                  mainAxisSpacing: 16,
                  crossAxisSpacing: 16,
                  childAspectRatio: 0.75, // Taller cards for images
                ),
                delegate: SliverChildBuilderDelegate((context, index) {
                  final strain = strains[index];
                  return StrainCard(
                    strain: strain,
                    onTap: () => _navigateToDetail(context, strain.id),
                  );
                }, childCount: strains.length),
              ),
            ),
            loading: () => const SliverFillRemaining(
              child: Center(child: CircularProgressIndicator.adaptive()),
            ),
            error: (err, stack) => SliverFillRemaining(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(
                      Icons.error_outline,
                      size: 48,
                      color: Colors.red,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      "Failed to load genetics",
                      style: Theme.of(context).textTheme.bodyLarge,
                    ),
                    TextButton(
                      onPressed: () => ref.refresh(geneticsLibraryProvider),
                      child: const Text("Retry"),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _navigateToDetail(BuildContext context, String strainId) {
    context.pushNamed('strain-detail', pathParameters: {'id': strainId});
  }
}
