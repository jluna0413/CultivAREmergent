import 'package:flutter/material.dart';

/// Sidebar Drawer Widget - Migrated from the original CultivAR web template
/// Replicates the complete sidebar menu structure and user experience
class SidebarDrawer extends StatelessWidget {
  const SidebarDrawer({
    super.key,
    required this.currentIndex,
    required this.onItemSelected,
    this.isAdmin = false,
  });
  final int currentIndex;
  final Function(int) onItemSelected;
  final bool isAdmin;

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: Container(
        color: const Color(0xFF2C5530), // Dark green background like original
        child: Column(
          children: [
            // Header with Logo
            _buildHeader(),

            // Main Menu Content
            Expanded(child: _buildMenuContent()),

            // Footer with Version
            _buildFooter(),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader() {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: const BoxDecoration(
        color: Color(0xFF1B3A1F), // Slightly darker green
        border: Border(bottom: BorderSide(color: Color(0xFF4CAF50), width: 1)),
      ),
      child: Row(
        children: [
          // Logo
          const Icon(Icons.eco, color: Color(0xFF4CAF50), size: 32),
          const SizedBox(width: 12),
          const Text(
            'CultivAR',
            style: TextStyle(
              color: Colors.white,
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const Spacer(),
          // Close button
          IconButton(
            icon: const Icon(Icons.close, color: Colors.white70),
            onPressed: () {
              // Close drawer - handled by Scaffold automatically
            },
          ),
        ],
      ),
    );
  }

  Widget _buildMenuContent() {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: ListView(
        children: [
          // Dashboard
          _buildMenuItem(
            index: 0,
            icon: Icons.dashboard,
            title: 'Dashboard',
            isActive: currentIndex == 0,
          ),

          // Plants
          _buildMenuItem(
            index: 1,
            icon: Icons.grass,
            title: 'Plants',
            isActive: currentIndex == 1,
          ),

          // Cultivars
          _buildMenuItem(
            index: 2,
            icon: Icons.science,
            title: 'Cultivars',
            isActive: currentIndex == 2,
          ),

          // Clone Management
          _buildMenuItem(
            index: 3,
            icon: Icons.account_tree,
            title: 'Clone Management',
            isActive: currentIndex == 3,
          ),

          // AI Features Section
          _buildExpandableMenuItem(
            icon: Icons.smart_toy,
            title: 'AI Features',
            children: [
              _buildSubMenuItem('AI Dashboard', 4, currentIndex == 4),
              _buildSubMenuItem('Plant Health Analysis', 5, currentIndex == 5),
              _buildSubMenuItem('Yield Prediction', 6, currentIndex == 6),
              _buildSubMenuItem('Grow Guidance', 7, currentIndex == 7),
              _buildSubMenuItem('Environmental Insights', 8, currentIndex == 8),
              _buildSubMenuItem('AI Chat Advisor', 9, currentIndex == 9),
            ],
          ),

          // Market Section
          _buildExpandableMenuItem(
            icon: Icons.store,
            title: 'Market',
            children: [
              _buildSubMenuItem('Seed Bank', 10, currentIndex == 10),
              _buildSubMenuItem('Extensions', 11, currentIndex == 11),
              _buildSubMenuItem('Gear', 12, currentIndex == 12),
            ],
          ),

          // Settings
          _buildMenuItem(
            index: 13,
            icon: Icons.settings,
            title: 'Settings',
            subtitle: '(Coming Soon)',
            isActive: currentIndex == 13,
            enabled: false,
          ),

          // Admin Section (if admin)
          if (isAdmin) ...[
            const Divider(color: Colors.white24, height: 32),
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
              child: Text(
                'ADMIN',
                style: TextStyle(
                  color: Colors.white70,
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                  letterSpacing: 1.2,
                ),
              ),
            ),
            _buildMenuItem(
              index: 14,
              icon: Icons.admin_panel_settings,
              title: 'User Management',
              isActive: currentIndex == 14,
            ),
            _buildMenuItem(
              index: 15,
              icon: Icons.download,
              title: 'Data Export',
              isActive: currentIndex == 15,
            ),
            _buildMenuItem(
              index: 16,
              icon: Icons.extension,
              title: 'Plugin Management',
              isActive: currentIndex == 16,
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildMenuItem({
    required int index,
    required IconData icon,
    required String title,
    String? subtitle,
    required bool isActive,
    bool enabled = true,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 2.0),
      decoration: BoxDecoration(
        color: isActive
            ? const Color(0xFF4CAF50).withAlpha(0x33)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(8.0),
        border: isActive
            ? const Border(left: BorderSide(color: Color(0xFF4CAF50), width: 3))
            : null,
      ),
      child: ListTile(
        leading: Icon(
          icon,
          color: isActive ? const Color(0xFF4CAF50) : Colors.white70,
        ),
        title: Text(
          title,
          style: TextStyle(
            color: isActive ? Colors.white : Colors.white70,
            fontWeight: isActive ? FontWeight.w600 : FontWeight.normal,
          ),
        ),
        subtitle: subtitle != null
            ? Text(
                subtitle,
                style: const TextStyle(color: Colors.white54, fontSize: 12),
              )
            : null,
        onTap: enabled ? () => onItemSelected(index) : null,
        enabled: enabled,
      ),
    );
  }

  Widget _buildExpandableMenuItem({
    required IconData icon,
    required String title,
    required List<Widget> children,
  }) {
    return Theme(
      data: ThemeData.dark().copyWith(dividerColor: Colors.transparent),
      child: ExpansionTile(
        leading: Icon(icon, color: Colors.white70),
        title: Text(
          title,
          style: const TextStyle(
            color: Colors.white70,
            fontWeight: FontWeight.w500,
          ),
        ),
        iconColor: Colors.white70,
        collapsedIconColor: Colors.white70,
        backgroundColor: const Color(0xFF1B3A1F).withAlpha(0x4D),
        collapsedBackgroundColor: Colors.transparent,
        children: children,
      ),
    );
  }

  Widget _buildSubMenuItem(String title, int index, bool isActive) {
    return Container(
      margin: const EdgeInsets.only(left: 16.0, right: 8.0, bottom: 2.0),
      decoration: BoxDecoration(
        color: isActive
            ? const Color(0xFF4CAF50).withAlpha(0x26)
            : Colors.transparent,
        borderRadius: BorderRadius.circular(6.0),
        border: isActive
            ? const Border(left: BorderSide(color: Color(0xFF4CAF50), width: 2))
            : null,
      ),
      child: ListTile(
        title: Text(
          title,
          style: TextStyle(
            color: isActive ? Colors.white : Colors.white60,
            fontSize: 14,
            fontWeight: isActive ? FontWeight.w600 : FontWeight.normal,
          ),
        ),
        onTap: () => onItemSelected(index),
        contentPadding: const EdgeInsets.only(left: 32.0),
        dense: true,
      ),
    );
  }

  Widget _buildFooter() {
    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: const BoxDecoration(
        border: Border(top: BorderSide(color: Colors.white12, width: 1)),
      ),
      child: const Text(
        'Version: 1.0.0',
        style: TextStyle(color: Colors.white54, fontSize: 12),
        textAlign: TextAlign.center,
      ),
    );
  }
}
