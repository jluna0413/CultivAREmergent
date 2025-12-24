import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:cultivar_app/core/providers/settings_provider.dart'
    as settings_provider;

/// Settings Screen - Comprehensive app settings and preferences
class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  @override
  Widget build(BuildContext context) {
    final settingsState = ref.watch(settings_provider.settingsProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        backgroundColor: const Color(0xFF4CAF50),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.restore),
            onPressed: () => _showResetConfirmation(context),
            tooltip: 'Reset to defaults',
          ),
        ],
      ),
      body: settingsState.isLoading == true
          ? const Center(
              child: CircularProgressIndicator(color: Color(0xFF4CAF50)),
            )
          : ListView(
              padding: const EdgeInsets.all(16),
              children: [
                // User Profile Section
                _buildUserProfileSection(),
                const SizedBox(height: 24),

                // Display Settings Section
                _buildDisplaySettingsSection(settingsState.settings.display),
                const SizedBox(height: 24),

                // Notification Settings Section
                _buildNotificationSettingsSection(
                  settingsState.settings.notifications,
                ),
                const SizedBox(height: 24),

                // Privacy & Security Section
                _buildPrivacySettingsSection(settingsState.settings.privacy),
                const SizedBox(height: 24),

                // App Management Section
                _buildAppManagementSection(settingsState),
                const SizedBox(height: 24),

                // About Section
                _buildAboutSection(settingsState.settings),
              ],
            ),
    );
  }

  Widget _buildUserProfileSection() {
    return _buildSectionCard(
      title: 'User Profile',
      icon: Icons.person,
      children: [
        ListTile(
          leading: const CircleAvatar(
            backgroundColor: Color(0xFF4CAF50),
            child: Icon(Icons.person, color: Colors.white),
          ),
          title: const Text('John Doe'),
          subtitle: const Text('john.doe@example.com'),
          trailing: IconButton(
            icon: const Icon(Icons.edit),
            onPressed: _editProfile,
          ),
        ),
      ],
    );
  }

  Widget _buildDisplaySettingsSection(
    settings_provider.DisplaySettings display,
  ) {
    return _buildSectionCard(
      title: 'Display & Appearance',
      icon: Icons.palette,
      children: [
        // Theme Selection
        ListTile(
          leading: const Icon(Icons.dark_mode),
          title: const Text('Theme'),
          subtitle: Text(_getThemeDisplayName(display.theme)),
          trailing: DropdownButton<String>(
            value: display.theme,
            onChanged: (String? newValue) {
              if (newValue != null) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Theme changed to: $newValue')),
                );
              }
            },
            items: const [
              DropdownMenuItem(value: 'system', child: Text('System')),
              DropdownMenuItem(value: 'light', child: Text('Light')),
              DropdownMenuItem(value: 'dark', child: Text('Dark')),
            ],
          ),
        ),

        // Language Selection
        ListTile(
          leading: const Icon(Icons.language),
          title: const Text('Language'),
          subtitle: Text(_getLanguageDisplayName(display.language)),
          trailing: DropdownButton<String>(
            value: display.language,
            onChanged: (String? newValue) {
              if (newValue != null) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Language changed to: $newValue')),
                );
              }
            },
            items: const [
              DropdownMenuItem(value: 'en', child: Text('English')),
              DropdownMenuItem(value: 'es', child: Text('Spanish')),
              DropdownMenuItem(value: 'fr', child: Text('French')),
            ],
          ),
        ),

        // Temperature Unit
        ListTile(
          leading: const Icon(Icons.thermostat),
          title: const Text('Temperature Unit'),
          subtitle: Text(
            display.temperatureUnit == 'celsius'
                ? 'Celsius (°C)'
                : 'Fahrenheit (°F)',
          ),
          trailing: Switch(
            value: display.temperatureUnit == 'celsius',
            onChanged: (value) {
              final unit = value ? 'celsius' : 'fahrenheit';
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Temperature unit changed to: $unit')),
              );
            },
            activeThumbColor: const Color(0xFF4CAF50),
          ),
        ),

        // Time Format
        ListTile(
          leading: const Icon(Icons.access_time),
          title: const Text('Time Format'),
          subtitle: Text(display.timeFormat == '24h' ? '24 Hour' : '12 Hour'),
          trailing: Switch(
            value: display.timeFormat == '24h',
            onChanged: (value) {
              final format = value ? '24h' : '12h';
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Time format changed to: $format')),
              );
            },
            activeThumbColor: const Color(0xFF4CAF50),
          ),
        ),

        // Compact Mode
        ListTile(
          leading: const Icon(Icons.density_small),
          title: const Text('Compact Mode'),
          subtitle: const Text('Use smaller UI elements'),
          trailing: Switch(
            value: display.compactMode,
            onChanged: (value) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Display settings updated')),
              );
            },
            activeThumbColor: const Color(0xFF4CAF50),
          ),
        ),

        // Auto Refresh
        ListTile(
          leading: const Icon(Icons.refresh),
          title: const Text('Auto Refresh'),
          subtitle: const Text('Automatically refresh data'),
          trailing: Switch(
            value: display.autoRefresh,
            onChanged: (value) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Display settings updated')),
              );
            },
            activeThumbColor: const Color(0xFF4CAF50),
          ),
        ),
      ],
    );
  }

  Widget _buildNotificationSettingsSection(
    settings_provider.NotificationSettings notifications,
  ) {
    return _buildSectionCard(
      title: 'Notifications',
      icon: Icons.notifications,
      children: [
        // Master Notification Toggle
        SwitchListTile(
          secondary: const Icon(Icons.notifications_active),
          title: const Text('Enable Notifications'),
          subtitle: const Text('Receive app notifications'),
          value: notifications.enabled,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Plant Alerts
        SwitchListTile(
          secondary: const Icon(Icons.eco),
          title: const Text('Plant Care Alerts'),
          subtitle: const Text('Watering, feeding reminders'),
          value: notifications.plantAlerts,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Harvest Reminders
        SwitchListTile(
          secondary: const Icon(Icons.calendar_today),
          title: const Text('Harvest Reminders'),
          subtitle: const Text('Harvest timing notifications'),
          value: notifications.harvestReminders,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Sensor Alerts
        SwitchListTile(
          secondary: const Icon(Icons.sensors),
          title: const Text('Sensor Alerts'),
          subtitle: const Text('Environmental monitoring alerts'),
          value: notifications.sensorAlerts,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Weekly Reports
        SwitchListTile(
          secondary: const Icon(Icons.analytics),
          title: const Text('Weekly Reports'),
          subtitle: const Text('Growth and analytics summaries'),
          value: notifications.weeklyReports,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Marketing Emails
        SwitchListTile(
          secondary: const Icon(Icons.email),
          title: const Text('Marketing Communications'),
          subtitle: const Text('Tips, news, and promotions'),
          value: notifications.marketingEmails,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Notification settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),
      ],
    );
  }

  Widget _buildPrivacySettingsSection(
    settings_provider.PrivacySettings privacy,
  ) {
    return _buildSectionCard(
      title: 'Privacy & Security',
      icon: Icons.security,
      children: [
        // Analytics
        SwitchListTile(
          secondary: const Icon(Icons.analytics),
          title: const Text('Usage Analytics'),
          subtitle: const Text('Help improve the app'),
          value: privacy.analyticsEnabled,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Crash Reporting
        SwitchListTile(
          secondary: const Icon(Icons.bug_report),
          title: const Text('Crash Reporting'),
          subtitle: const Text('Automatically report crashes'),
          value: privacy.crashReporting,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Data Sharing
        SwitchListTile(
          secondary: const Icon(Icons.share),
          title: const Text('Data Sharing'),
          subtitle: const Text('Share anonymized growing data'),
          value: privacy.dataSharing,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Location Services
        SwitchListTile(
          secondary: const Icon(Icons.location_on),
          title: const Text('Location Services'),
          subtitle: const Text('Enable for local weather data'),
          value: privacy.locationServices,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Biometric Authentication
        SwitchListTile(
          secondary: const Icon(Icons.fingerprint),
          title: const Text('Biometric Authentication'),
          subtitle: const Text('Use fingerprint/Face ID'),
          value: privacy.biometricAuth,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),

        // Auto Backup
        SwitchListTile(
          secondary: const Icon(Icons.backup),
          title: const Text('Auto Backup'),
          subtitle: const Text('Automatically backup app data'),
          value: privacy.autoBackup,
          onChanged: (value) {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Privacy settings updated')),
            );
          },
          activeThumbColor: const Color(0xFF4CAF50),
        ),
      ],
    );
  }

  Widget _buildAppManagementSection(
    settings_provider.SettingsProviderState state,
  ) {
    return _buildSectionCard(
      title: 'App Management',
      icon: Icons.storage,
      children: [
        ListTile(
          leading: const Icon(Icons.download),
          title: const Text('Export Data'),
          subtitle: const Text('Export your growing data'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _exportData,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.upload),
          title: const Text('Import Data'),
          subtitle: const Text('Import growing data backup'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _importData,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.clear_all),
          title: const Text('Clear Cache'),
          subtitle: const Text('Clear temporary app data'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _clearCache,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.delete_forever),
          title: const Text('Delete All Data'),
          subtitle: const Text('Remove all app data permanently'),
          trailing: const Icon(Icons.chevron_right),
          onTap: () => _showDeleteAllDataConfirmation(context),
        ),
      ],
    );
  }

  Widget _buildAboutSection(settings_provider.AppSettings settings) {
    return _buildSectionCard(
      title: 'About',
      icon: Icons.info,
      children: [
        ListTile(
          leading: const Icon(Icons.phone_android),
          title: const Text('App Version'),
          subtitle: Text('${settings.version} (${settings.buildNumber})'),
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.help),
          title: const Text('Help & Support'),
          subtitle: const Text('Get help and contact support'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _openHelpSupport,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.description),
          title: const Text('Terms of Service'),
          subtitle: const Text('View terms and conditions'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _openTermsOfService,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.privacy_tip),
          title: const Text('Privacy Policy'),
          subtitle: const Text('View privacy policy'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _openPrivacyPolicy,
        ),
        const Divider(),
        ListTile(
          leading: const Icon(Icons.rate_review),
          title: const Text('Rate App'),
          subtitle: const Text('Rate us on the app store'),
          trailing: const Icon(Icons.chevron_right),
          onTap: _rateApp,
        ),
      ],
    );
  }

  Widget _buildSectionCard({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
            child: Row(
              children: [
                Icon(icon, color: const Color(0xFF4CAF50)),
                const SizedBox(width: 12),
                Text(
                  title,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1),
          ...children,
        ],
      ),
    );
  }

  String _getThemeDisplayName(String theme) {
    switch (theme) {
      case 'system':
        return 'System Default';
      case 'light':
        return 'Light Theme';
      case 'dark':
        return 'Dark Theme';
      default:
        return theme;
    }
  }

  String _getLanguageDisplayName(String language) {
    switch (language) {
      case 'en':
        return 'English';
      case 'es':
        return 'Español';
      case 'fr':
        return 'Français';
      default:
        return language;
    }
  }

  void _editProfile() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Profile editing coming soon')),
    );
  }

  void _exportData() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Data export coming soon')));
  }

  void _importData() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Data import coming soon')));
  }

  void _clearCache() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Cache cleared')));
  }

  void _openHelpSupport() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Help & Support coming soon')));
  }

  void _openTermsOfService() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Terms of Service coming soon')),
    );
  }

  void _openPrivacyPolicy() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Privacy Policy coming soon')));
  }

  void _rateApp() {
    ScaffoldMessenger.of(
      context,
    ).showSnackBar(const SnackBar(content: Text('Rate App coming soon')));
  }

  void _showResetConfirmation(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Reset to Defaults'),
        content: const Text(
          'Are you sure you want to reset all settings to their default values?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Settings reset to defaults')),
              );
            },
            child: const Text('Reset'),
          ),
        ],
      ),
    );
  }

  void _showDeleteAllDataConfirmation(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete All Data'),
        content: const Text(
          'This will permanently delete all your growing data. This action cannot be undone. Are you sure?',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Data deletion feature coming soon'),
                ),
              );
            },
            child: const Text(
              'Delete All',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );
  }
}
