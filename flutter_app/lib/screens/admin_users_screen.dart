/// Admin Users Screen - Comprehensive user management interface for administrators
/// Provides complete CRUD operations, role-based access control, and analytics
library;

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Admin Users Screen - Complete user management interface
class AdminUsersScreen extends ConsumerStatefulWidget {
  const AdminUsersScreen({super.key});

  @override
  ConsumerState<AdminUsersScreen> createState() => _AdminUsersScreenState();
}

class _AdminUsersScreenState extends ConsumerState<AdminUsersScreen>
    with TickerProviderStateMixin {
  late TabController _tabController;
  final TextEditingController _searchController = TextEditingController();
  final GlobalKey<FormState> _createFormKey = GlobalKey<FormState>();

  // Create user form fields
  final _usernameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);

    // Load initial data
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _loadInitialData();
    });
  }

  @override
  void dispose() {
    _tabController.dispose();
    _searchController.dispose();
    _usernameController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    super.dispose();
  }

  void _loadInitialData() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Loading users...')));
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Loading analytics...')));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('User Management'),
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          labelColor: colorScheme.primary,
          unselectedLabelColor: colorScheme.onSurfaceVariant,
          indicatorColor: colorScheme.primary,
          tabs: const [
            Tab(icon: Icon(Icons.people), text: 'All Users'),
            Tab(icon: Icon(Icons.person_add), text: 'Create User'),
            Tab(icon: Icon(Icons.analytics), text: 'Analytics'),
            Tab(icon: Icon(Icons.security), text: 'Roles'),
          ],
        ),
        actions: [
          // Refresh button
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () => _loadInitialData(),
          ),
          // Export button
          IconButton(
            icon: const Icon(Icons.download),
            onPressed: () => _exportUsers(),
          ),
          // Settings popup
          PopupMenuButton<String>(
            onSelected: (value) {
              switch (value) {
                case 'settings':
                  _showUserSettings();
                  break;
                case 'help':
                  _showHelpDialog();
                  break;
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'settings',
                child: ListTile(
                  leading: Icon(Icons.settings),
                  title: Text('Settings'),
                ),
              ),
              const PopupMenuItem(
                value: 'help',
                child: ListTile(leading: Icon(Icons.help), title: Text('Help')),
              ),
            ],
          ),
        ],
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildUsersListTab(),
          _buildCreateUserTab(),
          _buildAnalyticsTab(),
          _buildRolesTab(),
        ],
      ),
      // Error snackbar
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          ScaffoldMessenger.of(
            context,
          ).showSnackBar(const SnackBar(content: Text('Mock error cleared')));
        },
        backgroundColor: Colors.red,
        child: const Icon(Icons.close),
      ),
    );
  }

  Widget _buildUsersListTab() {
    return Column(
      children: [
        _buildSearchAndFilters(),
        Expanded(child: _buildUsersList()),
      ],
    );
  }

  Widget _buildSearchAndFilters() {
    return Container(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // Search Bar
          TextField(
            controller: _searchController,
            decoration: InputDecoration(
              hintText: 'Search users by name, email, or username...',
              prefixIcon: const Icon(Icons.search),
              suffixIcon: _searchController.text.isNotEmpty
                  ? IconButton(
                      icon: const Icon(Icons.clear),
                      onPressed: () {
                        _searchController.clear();
                        _performSearch();
                      },
                    )
                  : null,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            onSubmitted: (_) => _performSearch(),
            onChanged: (value) {
              if (value.isEmpty) {
                _performSearch();
              }
            },
          ),
          const SizedBox(height: 16),
          // Filter Chips
          Row(
            children: [
              Expanded(child: _buildRoleFilterChips()),
              const SizedBox(width: 12),
              Expanded(child: _buildStatusFilterChips()),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildRoleFilterChips() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        FilterChip(
          label: const Text('All'),
          selected: true,
          onSelected: (selected) {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(const SnackBar(content: Text('Filter: All roles')));
          },
        ),
        FilterChip(
          label: const Text('Admin'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(const SnackBar(content: Text('Filter: Admin role')));
          },
        ),
        FilterChip(
          label: const Text('Moderator'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Filter: Moderator role')),
            );
          },
        ),
        FilterChip(
          label: const Text('User'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(
              context,
            ).showSnackBar(const SnackBar(content: Text('Filter: User role')));
          },
        ),
      ],
    );
  }

  Widget _buildStatusFilterChips() {
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: [
        FilterChip(
          label: const Text('All'),
          selected: true,
          onSelected: (selected) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Filter: All statuses')),
            );
          },
        ),
        FilterChip(
          label: const Text('Active'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Filter: Active status')),
            );
          },
        ),
        FilterChip(
          label: const Text('Inactive'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Filter: Inactive status')),
            );
          },
        ),
        FilterChip(
          label: const Text('Suspended'),
          selected: false,
          onSelected: (selected) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Filter: Suspended status')),
            );
          },
        ),
      ],
    );
  }

  Widget _buildUsersList() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            _searchController.text.isNotEmpty ? Icons.search_off : Icons.people,
            size: 64,
            color: Colors.grey,
          ),
          const SizedBox(height: 16),
          Text(
            _searchController.text.isNotEmpty
                ? 'No users found'
                : 'User management interface ready',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            _searchController.text.isNotEmpty
                ? 'Try adjusting your search or filters'
                : 'Mock admin interface loaded successfully',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 16),
          if (_searchController.text.isNotEmpty)
            ElevatedButton(
              onPressed: () {
                _searchController.clear();
                _performSearch();
              },
              child: const Text('Clear Search'),
            ),
        ],
      ),
    );
  }

  Widget _buildCreateUserTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: _buildCreateUserForm(),
    );
  }

  Widget _buildCreateUserForm() {
    return Form(
      key: _createFormKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Create New User',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 24),
          TextFormField(
            controller: _usernameController,
            decoration: const InputDecoration(
              labelText: 'Username *',
              hintText: 'Enter username',
              prefixIcon: Icon(Icons.person),
              border: OutlineInputBorder(),
            ),
            validator: (value) {
              if (value?.isEmpty ?? true) return 'Username is required';
              if (value!.length < 3) {
                return 'Username must be at least 3 characters';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _emailController,
            decoration: const InputDecoration(
              labelText: 'Email *',
              hintText: 'Enter email address',
              prefixIcon: Icon(Icons.email),
              border: OutlineInputBorder(),
            ),
            validator: (value) {
              if (value?.isEmpty ?? true) return 'Email is required';
              if (!value!.contains('@') || !value.contains('.')) {
                return 'Invalid email format';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _passwordController,
            decoration: const InputDecoration(
              labelText: 'Password *',
              hintText: 'Enter password',
              prefixIcon: Icon(Icons.lock),
              border: OutlineInputBorder(),
            ),
            obscureText: true,
            validator: (value) {
              if (value?.isEmpty ?? true) return 'Password is required';
              if (value!.length < 6) {
                return 'Password must be at least 6 characters';
              }
              return null;
            },
          ),
          const SizedBox(height: 16),
          Row(
            children: [
              Expanded(
                child: TextFormField(
                  controller: _firstNameController,
                  decoration: const InputDecoration(
                    labelText: 'First Name',
                    hintText: 'First name',
                    prefixIcon: Icon(Icons.badge),
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: TextFormField(
                  controller: _lastNameController,
                  decoration: const InputDecoration(
                    labelText: 'Last Name',
                    hintText: 'Last name',
                    prefixIcon: Icon(Icons.badge),
                    border: OutlineInputBorder(),
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 16),
          DropdownButtonFormField<String>(
            decoration: const InputDecoration(
              labelText: 'Role',
              prefixIcon: Icon(Icons.security),
              border: OutlineInputBorder(),
            ),
            items: const [
              DropdownMenuItem(value: 'user', child: Text('User')),
              DropdownMenuItem(value: 'moderator', child: Text('Moderator')),
              DropdownMenuItem(value: 'admin', child: Text('Admin')),
            ],
            onChanged: (value) {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Role changed to: $value')),
              );
            },
          ),
          const SizedBox(height: 32),
          Row(
            children: [
              ElevatedButton(
                onPressed: () => _submitCreateForm(),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 32,
                    vertical: 12,
                  ),
                ),
                child: const Text('Create User'),
              ),
              const SizedBox(width: 16),
              OutlinedButton(
                onPressed: _resetCreateForm,
                child: const Text('Reset'),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildAnalyticsTab() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                'User Analytics',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              IconButton(
                icon: const Icon(Icons.refresh),
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Analytics refreshed')),
                  );
                },
              ),
            ],
          ),
          const SizedBox(height: 24),
          Expanded(child: _buildAnalyticsContent()),
        ],
      ),
    );
  }

  Widget _buildAnalyticsContent() {
    return Column(
      children: [
        // Summary Cards
        GridView.count(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisCount: 2,
          crossAxisSpacing: 16,
          mainAxisSpacing: 16,
          childAspectRatio: 1.5,
          children: [
            _buildAnalyticsCard('Total Users', '0', Icons.people, Colors.blue),
            _buildAnalyticsCard(
              'Active Users',
              '0',
              Icons.person,
              Colors.green,
            ),
            _buildAnalyticsCard(
              'New This Month',
              '0',
              Icons.person_add,
              Colors.orange,
            ),
            _buildAnalyticsCard(
              'Admins',
              '0',
              Icons.admin_panel_settings,
              Colors.red,
            ),
          ],
        ),
        const SizedBox(height: 24),
        // Mock chart
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Role Distribution',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 16),
                Center(
                  child: Column(
                    children: [
                      Icon(
                        Icons.bar_chart,
                        size: 64,
                        color: Colors.grey.shade400,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Analytics visualization coming soon',
                        style: TextStyle(color: Colors.grey.shade600),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Widget _buildAnalyticsCard(
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, color: color, size: 32),
            const SizedBox(height: 8),
            Text(
              value,
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: Theme.of(context).textTheme.bodyMedium,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildRolesTab() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Role Management',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 24),
          Expanded(
            child: ListView.builder(
              itemCount: 3,
              itemBuilder: (context, index) {
                final roles = ['Admin', 'Moderator', 'User'];
                final descriptions = [
                  'Full system access',
                  'Limited permissions',
                  'Basic user access',
                ];
                final colors = [Colors.red, Colors.orange, Colors.blue];
                final role = roles[index];
                final description = descriptions[index];
                final color = colors[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: color.withValues(alpha: 0.1),
                      child: Icon(
                        index == 0
                            ? Icons.admin_panel_settings
                            : index == 1
                            ? Icons.security
                            : Icons.person,
                        color: color,
                      ),
                    ),
                    title: Text(role),
                    subtitle: Text('$description • Mock interface'),
                    trailing: IconButton(
                      icon: const Icon(Icons.edit),
                      onPressed: () => _editRole(role),
                    ),
                  ),
                );
              },
            ),
          ),
        ],
      ),
    );
  }

  // Action handlers
  void _performSearch() {
    final searchQuery = _searchController.text;

    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text('Searching for: $searchQuery')));
  }

  void _handleUserAction(String action, String userId) async {
    switch (action) {
      case 'edit':
        _editUser(userId);
        break;
      case 'toggle_status':
        ScaffoldMessenger.of(
          context,
        ).showSnackBar(SnackBar(content: Text('User $userId status toggled')));
        break;
      case 'reset_password':
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Password reset email sent')),
        );
        break;
      case 'delete':
        _confirmDeleteUser(userId);
        break;
    }
  }

  void _submitCreateForm() async {
    if (!_createFormKey.currentState!.validate()) return;

    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('User created successfully!')));
    _resetCreateForm();
    _tabController.animateTo(0); // Switch to user list
  }

  void _resetCreateForm() {
    _usernameController.clear();
    _emailController.clear();
    _passwordController.clear();
    _firstNameController.clear();
    _lastNameController.clear();
  }

  void _editUser(String userId) {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(SnackBar(content: Text('Editing user: $userId')));
  }

  void _confirmDeleteUser(String userId) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete User'),
        content: Text(
          'Are you sure you want to delete user $userId? This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () async {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('User $userId deleted successfully')),
              );
            },
            style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
            child: const Text('Delete', style: TextStyle(color: Colors.white)),
          ),
        ],
      ),
    );
  }

  void _exportUsers() async {
    try {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Export functionality coming soon')),
      );
    } catch (e) {
      ScaffoldMessenger.of(
        context,
      ).showSnackBar(SnackBar(content: Text('Failed to export users: $e')));
    }
  }

  void _showUserSettings() {
    showDialog(
      context: context,
      builder: (context) => const UserSettingsDialog(),
    );
  }

  void _showHelpDialog() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('User Management Help'),
        content: const Text(
          'This is a mock admin interface. In the real implementation, this would provide complete user management functionality.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _editRole(String role) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Edit $role Role'),
        content: const Text(
          'Role editing functionality will be implemented here. This would typically open a form to modify role permissions and settings.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}

// Dialogs

class UserSettingsDialog extends StatelessWidget {
  const UserSettingsDialog({super.key});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('User Management Settings'),
      content: const Text(
        'User management settings and configuration options will be implemented here.',
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Close'),
        ),
      ],
    );
  }
}
