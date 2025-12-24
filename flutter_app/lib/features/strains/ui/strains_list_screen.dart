// Cultivars list screen
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../core/models/cultivar_models.dart';
import '../../../core/services/cultivars_api_service.dart';
import '../../../core/providers/cultivar_provider.dart' as cultivar_provider;
import '../../../core/theme/app_navigation_drawer.dart';

class StrainsListScreen extends StatefulWidget {
  const StrainsListScreen({super.key});

  @override
  State<StrainsListScreen> createState() => _StrainsListScreenState();
}

class _StrainsListScreenState extends State<StrainsListScreen> {
  List<cultivar_provider.ExtendedCultivar> _cultivars = [];
  CultivarStats? _stats;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadCultivars();
  }

  Future<void> _loadCultivars() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final cultivars = await CultivarsApiService.getCultivars();
      final extendedCultivars = cultivars
          .map((c) => cultivar_provider.ExtendedCultivar.fromBase(c))
          .toList();
      final stats = await CultivarsApiService.getCultivarStats();

      setState(() {
        _cultivars = extendedCultivars;
        _stats = stats;
        _isLoading = false;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        _isLoading = false;
      });
    }
  }

  Future<void> _refreshCultivars() async {
    await _loadCultivars();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      backgroundColor: const Color(0xFF1a1a1a),
      appBar: AppBar(
        backgroundColor: const Color(0xFF2a2a2a),
        title: const Text('My Strains', style: TextStyle(color: Colors.white)),
        iconTheme: const IconThemeData(color: Colors.white),
        leading: IconButton(
          icon: const Icon(Icons.arrow_back),
          onPressed: () => context.go('/dashboard'),
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _refreshCultivars,
            color: Colors.white,
          ),
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _navigateToCreateCultivar(),
            color: Colors.white,
          ),
        ],
      ),
      drawer: const AppNavigationDrawer(),
      body: _buildBody(theme),
      floatingActionButton: FloatingActionButton(
        onPressed: () => _navigateToCreateCultivar(),
        backgroundColor: const Color(0xFF4CAF50),
        child: const Icon(Icons.add, color: Colors.white),
      ),
    );
  }

  Widget _buildBody(ThemeData theme) {
    if (_isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_error != null) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.error_outline, size: 64, color: Colors.red),
            const SizedBox(height: 16),
            Text(
              'Error loading cultivars',
              style: theme.textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              _error!,
              style: theme.textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _loadCultivars,
              child: const Text('Try Again'),
            ),
          ],
        ),
      );
    }

    if (_cultivars.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.eco, size: 64, color: Colors.grey),
            const SizedBox(height: 16),
            Text('No Cultivars Yet', style: theme.textTheme.headlineSmall),
            const SizedBox(height: 8),
            Text(
              'Start building your cultivar collection by adding your first strain.',
              style: theme.textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => _navigateToCreateCultivar(),
              icon: const Icon(Icons.add),
              label: const Text('Add Your First Cultivar'),
              style: ElevatedButton.styleFrom(
                backgroundColor: const Color(0xFF4CAF50),
                foregroundColor: Colors.white,
              ),
            ),
          ],
        ),
      );
    }

    return RefreshIndicator(
      onRefresh: _refreshCultivars,
      child: CustomScrollView(
        slivers: [
          if (_stats != null) _buildStatsSection(),
          _buildCultivarsList(),
        ],
      ),
    );
  }

  Widget _buildStatsSection() {
    return SliverToBoxAdapter(
      child: Container(
        margin: const EdgeInsets.all(16),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF4CAF50).withAlpha(0x33),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Collection Overview',
              style: Theme.of(
                context,
              ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: _buildStatItem(
                    'Total',
                    '${_stats!.totalCultivars}',
                    Icons.category,
                  ),
                ),
                Expanded(
                  child: _buildStatItem(
                    'Autoflower',
                    '${_stats!.autoflower}',
                    Icons.timer,
                  ),
                ),
                Expanded(
                  child: _buildStatItem(
                    'Photoperiod',
                    '${_stats!.photoperiod}',
                    Icons.light_mode,
                  ),
                ),
              ],
            ),
            if (_stats!.mostUsedCultivar != null) ...[
              const SizedBox(height: 12),
              Text(
                'Most Used: ${_stats!.mostUsedCultivar} (${_stats!.mostUsedCount} plants)',
                style: Theme.of(context).textTheme.bodySmall?.copyWith(
                  fontStyle: FontStyle.italic,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }

  Widget _buildStatItem(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, size: 24, color: const Color(0xFF4CAF50)),
        const SizedBox(height: 4),
        Text(
          value,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: Color(0xFF4CAF50),
          ),
        ),
        Text(label, style: TextStyle(fontSize: 12, color: Colors.grey[600])),
      ],
    );
  }

  Widget _buildCultivarsList() {
    return SliverList(
      delegate: SliverChildBuilderDelegate((context, index) {
        final cultivar = _cultivars[index];
        return _buildCultivarCard(cultivar);
      }, childCount: _cultivars.length),
    );
  }

  Widget _buildCultivarCard(cultivar_provider.ExtendedCultivar cultivar) {
    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: InkWell(
        onTap: () => _navigateToCultivarDetail(cultivar),
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header with name and type badges
              Row(
                children: [
                  Expanded(
                    child: Text(
                      cultivar.name,
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  if (cultivar.autoflower)
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.blue.withAlpha(0x1A),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.blue.withAlpha(0x4D)),
                      ),
                      child: const Text(
                        'Auto',
                        style: TextStyle(
                          fontSize: 12,
                          color: Colors.blue,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 8,
                      vertical: 4,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF4CAF50).withAlpha(0x1A),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      cultivar.type == cultivar_provider.CultivarType.indica
                          ? '100% Indica'
                          : (cultivar.type ==
                                    cultivar_provider.CultivarType.sativa
                                ? '100% Sativa'
                                : 'Hybrid'),
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                        color: Color(0xFF4CAF50),
                      ),
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              // Breeder
              if (cultivar.breederName != null) ...[
                Row(
                  children: [
                    const Icon(Icons.business, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text(
                      cultivar.breederName!,
                      style: TextStyle(color: Colors.grey[600], fontSize: 14),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
              ],

              // Cycle time
              if (cultivar.cycleTime != null) ...[
                Row(
                  children: [
                    const Icon(Icons.timer, size: 16, color: Colors.grey),
                    const SizedBox(width: 4),
                    Text(
                      '${cultivar.cycleTime} days flowering',
                      style: TextStyle(color: Colors.grey[600], fontSize: 14),
                    ),
                  ],
                ),
                const SizedBox(height: 4),
              ],

              // Seed count and plant count
              Row(
                children: [
                  const Icon(Icons.inventory_2, size: 16, color: Colors.grey),
                  const SizedBox(width: 4),
                  Text(
                    '${cultivar.seedCount} seeds',
                    style: TextStyle(color: Colors.grey[600], fontSize: 14),
                  ),
                  const SizedBox(width: 16),
                  const Icon(Icons.eco, size: 16, color: Colors.grey),
                  const SizedBox(width: 4),
                  Text(
                    '${cultivar.plantCount} plants',
                    style: TextStyle(color: Colors.grey[600], fontSize: 14),
                  ),
                ],
              ),

              const SizedBox(height: 8),

              // Description
              if (cultivar.shortDescription != null) ...[
                Text(
                  cultivar.shortDescription!,
                  style: TextStyle(color: Colors.grey[700], fontSize: 14),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),
              ],

              // Actions
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  TextButton.icon(
                    onPressed: () => _navigateToEditCultivar(cultivar),
                    icon: const Icon(Icons.edit, size: 16),
                    label: const Text('Edit'),
                    style: TextButton.styleFrom(
                      foregroundColor: const Color(0xFF4CAF50),
                    ),
                  ),
                  const SizedBox(width: 8),
                  TextButton.icon(
                    onPressed: () => _navigateToCultivarDetail(cultivar),
                    icon: const Icon(Icons.info, size: 16),
                    label: const Text('Details'),
                    style: TextButton.styleFrom(foregroundColor: Colors.blue),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _navigateToCreateCultivar() {
    context.go('/strains/new');
  }

  void _navigateToEditCultivar(cultivar_provider.ExtendedCultivar cultivar) {
    Navigator.of(
      context,
    ).pushNamed('/cultivars/edit', arguments: cultivar.base);
  }

  void _navigateToCultivarDetail(cultivar_provider.ExtendedCultivar cultivar) {
    Navigator.of(
      context,
    ).pushNamed('/cultivars/detail', arguments: cultivar.base);
  }
}
