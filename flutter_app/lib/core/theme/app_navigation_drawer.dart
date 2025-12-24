import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../providers/auth_provider.dart';
import 'app_colors.dart';

/// Navigation Drawer for CultivAR app
/// Provides access to all major app sections organized by category
class AppNavigationDrawer extends ConsumerWidget {
  const AppNavigationDrawer({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final isAdmin = authState.when(
      data: (s) => s.user?.isAdmin ?? false,
      loading: () => false,
      error: (_, __) => false,
    );
    final currentPath = GoRouterState.of(context).uri.path;

    return Drawer(
      backgroundColor: const Color(0xFF1a1a1a),
      child: Column(
        children: [
          // Header with user info
          _buildDrawerHeader(context),

          // Navigation items
          Expanded(
            child: ListView(
              padding: EdgeInsets.zero,
              children: [
                // Core Features
                _buildSectionHeader('Core'),
                _buildNavItem(
                  context,
                  icon: Icons.dashboard,
                  label: 'Dashboard',
                  route: '/dashboard',
                  isSelected: currentPath == '/dashboard',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.local_florist,
                  label: 'Plants',
                  route: '/plants',
                  isSelected: currentPath.startsWith('/plants'),
                ),
                _buildNavItem(
                  context,
                  icon: Icons.science,
                  label: 'Strains',
                  route: '/strains',
                  isSelected: currentPath.startsWith('/strains'),
                ),
                _buildNavItem(
                  context,
                  icon: Icons.content_copy,
                  label: 'Clones',
                  route: '/clones',
                  isSelected: currentPath == '/clones',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.sensors,
                  label: 'Sensors',
                  route: '/sensors',
                  isSelected: currentPath.startsWith('/sensors'),
                ),

                const Divider(color: Colors.white24),

                // Nutrients
                _buildSectionHeader('Nutrients'),
                _buildNavItem(
                  context,
                  icon: Icons.science_outlined,
                  label: 'Calculator',
                  route: '/nutrients/calculator',
                  isSelected: currentPath == '/nutrients/calculator',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.inventory_2_outlined,
                  label: 'Inventory',
                  route: '/nutrients/inventory',
                  isSelected: currentPath == '/nutrients/inventory',
                ),

                const Divider(color: Colors.white24),

                // Marketplace
                _buildSectionHeader('Marketplace'),
                _buildNavItem(
                  context,
                  icon: Icons.grain,
                  label: 'Seed Bank',
                  route: '/market/seedbank',
                  isSelected: currentPath == '/market/seedbank',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.build,
                  label: 'Gear',
                  route: '/market/gear',
                  isSelected: currentPath == '/market/gear',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.extension,
                  label: 'Extensions',
                  route: '/market/extensions',
                  isSelected: currentPath == '/market/extensions',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.shopping_cart,
                  label: 'Cart',
                  route: '/cart',
                  isSelected: currentPath == '/cart',
                ),

                const Divider(color: Colors.white24),

                // AI Features
                _buildSectionHeader('AI Assistant'),
                // Agent Hub - only visible to admin users
                if (isAdmin) ...[
                  _buildNavItem(
                    context,
                    icon: Icons.hub_outlined, // Use a hub-like icon
                    label: 'Agent Hub',
                    route: '/ai/hub',
                    isSelected: currentPath == '/ai/hub',
                  ),
                ],
                _buildNavItem(
                  context,
                  icon: Icons.psychology,
                  label: 'AI Dashboard',
                  route: '/ai',
                  isSelected: currentPath == '/ai',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.chat,
                  label: 'Chat Advisor',
                  route: '/ai/chat',
                  isSelected: currentPath == '/ai/chat',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.thermostat,
                  label: 'Environment',
                  route: '/ai/insights',
                  isSelected: currentPath == '/ai/insights',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.medical_services,
                  label: 'Health Analysis',
                  route: '/ai/health',
                  isSelected: currentPath == '/ai/health',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.trending_up,
                  label: 'Yield Prediction',
                  route: '/ai/yield',
                  isSelected: currentPath == '/ai/yield',
                ),

                const Divider(color: Colors.white24),

                // Admin (only show if user is admin)
                _buildSectionHeader('Admin'),
                _buildNavItem(
                  context,
                  icon: Icons.admin_panel_settings,
                  label: 'Admin Dashboard',
                  route: '/admin',
                  isSelected: currentPath == '/admin',
                ),
                _buildNavItem(
                  context,
                  icon: Icons.people,
                  label: 'User Management',
                  route: '/admin/users',
                  isSelected: currentPath == '/admin/users',
                ),

                const Divider(color: Colors.white24),

                // Settings
                _buildNavItem(
                  context,
                  icon: Icons.settings,
                  label: 'Settings',
                  route: '/settings',
                  isSelected: currentPath == '/settings',
                ),
              ],
            ),
          ),

          // Footer with logout
          _buildDrawerFooter(context, ref),
        ],
      ),
    );
  }

  Widget _buildDrawerHeader(BuildContext context) {
    return DrawerHeader(
      decoration: const BoxDecoration(
        gradient: LinearGradient(
          colors: [AppColors.primary600, AppColors.primary500],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const CircleAvatar(
            radius: 30,
            backgroundColor: Colors.white24,
            child: Icon(Icons.local_florist, size: 32, color: Colors.white),
          ),
          const SizedBox(height: 12),
          const Text(
            'CultivAR',
            style: TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            'Grow Smart, Grow Better',
            style: TextStyle(
              color: Colors.white.withOpacity(0.8),
              fontSize: 14,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title.toUpperCase(),
        style: TextStyle(
          color: Colors.white.withOpacity(0.5),
          fontSize: 12,
          fontWeight: FontWeight.w600,
          letterSpacing: 1.2,
        ),
      ),
    );
  }

  Widget _buildNavItem(
    BuildContext context, {
    required IconData icon,
    required String label,
    required String route,
    required bool isSelected,
  }) {
    return ListTile(
      leading: Icon(
        icon,
        color: isSelected ? AppColors.primary500 : Colors.white70,
      ),
      title: Text(
        label,
        style: TextStyle(
          color: isSelected ? AppColors.primary500 : Colors.white,
          fontWeight: isSelected ? FontWeight.w600 : FontWeight.normal,
        ),
      ),
      selected: isSelected,
      selectedTileColor: AppColors.primary500.withOpacity(0.1),
      onTap: () {
        Navigator.pop(context); // Close drawer
        context.go(route);
      },
    );
  }

  Widget _buildDrawerFooter(BuildContext context, WidgetRef ref) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border(top: BorderSide(color: Colors.white.withOpacity(0.1))),
      ),
      child: ListTile(
        leading: const Icon(Icons.logout, color: Colors.redAccent),
        title: const Text(
          'Sign Out',
          style: TextStyle(color: Colors.redAccent),
        ),
        onTap: () {
          // Sign out and navigate to login
          ref.read(authProvider.notifier).logout();
          context.go('/login');
        },
      ),
    );
  }
}
