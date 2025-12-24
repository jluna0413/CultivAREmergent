/// FilterBar widget for filter controls
/// Matches the filter-bar design from plants.html, strains.html, and sensors.html
library;
// (removed stray library directive)

import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

/// Configuration for individual filter fields
class FilterConfig {
  const FilterConfig({
    required this.label,
    this.type = FilterType.dropdown,
    this.options,
    this.initialValue,
    this.hint,
    this.searchHint,
  });

  final String label;
  final FilterType type;
  final List<String>? options;
  final String? initialValue;
  final String? hint;
  final String? searchHint;
}

enum FilterType { dropdown, text, date, checkbox, multiselect }

class FilterBar extends StatefulWidget {
  const FilterBar({
    super.key,
    required this.filters,
    this.onFilterChanged,
    this.onReset,
    this.compact = false,
  });

  final List<FilterConfig> filters;
  final void Function(Map<String, dynamic> filters)? onFilterChanged;
  final VoidCallback? onReset;
  final bool compact;

  @override
  State<FilterBar> createState() => _FilterBarState();
}

class _FilterBarState extends State<FilterBar> {
  final Map<String, dynamic> _currentFilters = {};
  final Map<String, TextEditingController> _controllers = {};

  @override
  void initState() {
    super.initState();
    _initializeFilters();
  }

  void _initializeFilters() {
    for (final filter in widget.filters) {
      _currentFilters[filter.label] = filter.initialValue;

      if (filter.type == FilterType.text) {
        _controllers[filter.label] = TextEditingController(
          text: filter.initialValue ?? '',
        );
      }
    }
  }

  @override
  void dispose() {
    for (final controller in _controllers.values) {
      controller.dispose();
    }
    super.dispose();
  }

  void _updateFilter(String key, dynamic value) {
    setState(() {
      _currentFilters[key] = value;
    });
    widget.onFilterChanged?.call(Map.from(_currentFilters));
  }

  void _resetFilters() {
    setState(() {
      _currentFilters.clear();
      for (final filter in widget.filters) {
        _currentFilters[filter.label] = null;
        if (filter.type == FilterType.text) {
          _controllers[filter.label]?.clear();
        }
      }
    });
    widget.onReset?.call();
    widget.onFilterChanged?.call(_currentFilters);
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDark = theme.brightness == Brightness.dark;

    return Container(
      decoration: BoxDecoration(
        color: isDark
            ? AppTheme.surfaceColor.withValues(alpha: 0.8)
            : const Color(0xB3FFFFFF),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isDark
              ? AppTheme.borderColor.withValues(alpha: 0.2)
              : AppTheme.borderSecondary.withValues(alpha: 0.1),
          width: 1,
        ),
        boxShadow: const [
          BoxShadow(
            color: Color(0x1A000000),
            offset: Offset(0, 2),
            blurRadius: 4,
            spreadRadius: 0,
          ),
        ],
      ),
      child: Padding(
        padding: widget.compact
            ? const EdgeInsets.all(16)
            : const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Filter Bar Header
            Row(
              children: [
                Icon(
                  Icons.filter_list,
                  color: AppTheme.primaryColor,
                  size: widget.compact ? 18 : 20,
                ),
                const SizedBox(width: 8),
                Text(
                  'Filters',
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const Spacer(),
                if (widget.onReset != null)
                  TextButton.icon(
                    onPressed: _resetFilters,
                    icon: const Icon(Icons.clear_all, size: 16),
                    label: const Text('Reset'),
                    style: TextButton.styleFrom(
                      foregroundColor: AppTheme.textSecondary,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 8,
                        vertical: 4,
                      ),
                    ),
                  ),
              ],
            ),
            const SizedBox(height: 16),

            // Filter Controls
            LayoutBuilder(
              builder: (context, constraints) {
                return Wrap(
                  spacing: 16,
                  runSpacing: 12,
                  children: widget.filters.map((filter) {
                    return _buildFilterControl(
                      context,
                      filter,
                      constraints.maxWidth,
                    );
                  }).toList(),
                );
              },
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildFilterControl(
    BuildContext context,
    FilterConfig filter,
    double maxWidth,
  ) {
    final theme = Theme.of(context);
    // Calculate width based on screen size and content
    final bool isSmallScreen = maxWidth < 600;
    final double filterWidth;

    switch (filter.type) {
      case FilterType.dropdown:
        filterWidth = isSmallScreen ? maxWidth - 32 : 200;
        break;
      case FilterType.text:
        filterWidth = isSmallScreen ? maxWidth - 32 : 250;
        break;
      case FilterType.date:
        filterWidth = isSmallScreen ? (maxWidth - 48) / 2 : 180;
        break;
      case FilterType.checkbox:
        filterWidth = 120;
        break;
      default:
        filterWidth = 200;
    }

    switch (filter.type) {
      case FilterType.dropdown:
        return _buildDropdownFilter(filter, theme, filterWidth);
      case FilterType.text:
        return _buildTextFilter(filter, theme, filterWidth);
      case FilterType.date:
        return _buildDateFilter(filter, theme, filterWidth);
      case FilterType.checkbox:
        return _buildCheckboxFilter(filter, theme);
      case FilterType.multiselect:
        return _buildMultiselectFilter(filter, theme, filterWidth);
    }
  }

  Widget _buildDropdownFilter(
    FilterConfig filter,
    ThemeData theme,
    double width,
  ) {
    final currentValue = _currentFilters[filter.label];

    return SizedBox(
      width: width,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            filter.label,
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.textSecondary,
            ),
          ),
          const SizedBox(height: 6),
          DropdownButtonFormField<String>(
            initialValue: currentValue,
            decoration: InputDecoration(
              hintText: filter.hint ?? 'Select ${filter.label.toLowerCase()}',
              hintStyle: TextStyle(
                color: AppTheme.textSecondary.withValues(alpha: 0.7),
              ),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: const BorderSide(
                  color: AppTheme.primaryColor,
                  width: 2,
                ),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 10,
              ),
              filled: true,
              fillColor: AppTheme.surfaceColor,
            ),
            items: (filter.options ?? []).map((option) {
              return DropdownMenuItem(value: option, child: Text(option));
            }).toList(),
            onChanged: (value) => _updateFilter(filter.label, value),
            isExpanded: true,
          ),
        ],
      ),
    );
  }

  Widget _buildTextFilter(FilterConfig filter, ThemeData theme, double width) {
    final controller = _controllers[filter.label]!;

    return SizedBox(
      width: width,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            filter.label,
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.textSecondary,
            ),
          ),
          const SizedBox(height: 6),
          TextFormField(
            controller: controller,
            decoration: InputDecoration(
              hintText:
                  filter.searchHint ??
                  'Search ${filter.label.toLowerCase()}...',
              hintStyle: TextStyle(
                color: AppTheme.textSecondary.withValues(alpha: 0.7),
              ),
              prefixIcon: const Icon(Icons.search),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: const BorderSide(
                  color: AppTheme.primaryColor,
                  width: 2,
                ),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 10,
              ),
              filled: true,
              fillColor: AppTheme.surfaceColor,
            ),
            onChanged: (value) => _updateFilter(filter.label, value),
          ),
        ],
      ),
    );
  }

  Widget _buildDateFilter(FilterConfig filter, ThemeData theme, double width) {
    final currentValue = _currentFilters[filter.label] as DateTime?;

    return SizedBox(
      width: width,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            filter.label,
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.textSecondary,
            ),
          ),
          const SizedBox(height: 6),
          TextFormField(
            readOnly: true,
            decoration: InputDecoration(
              hintText: currentValue != null
                  ? '${currentValue.day}/${currentValue.month}/${currentValue.year}'
                  : filter.hint ?? 'Select date',
              hintStyle: TextStyle(
                color: AppTheme.textSecondary.withValues(alpha: 0.7),
              ),
              prefixIcon: const Icon(Icons.calendar_today),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              enabledBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: BorderSide(
                  color: AppTheme.borderColor.withValues(alpha: 0.3),
                ),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(8),
                borderSide: const BorderSide(
                  color: AppTheme.primaryColor,
                  width: 2,
                ),
              ),
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 12,
                vertical: 10,
              ),
              filled: true,
              fillColor: AppTheme.surfaceColor,
            ),
            onTap: () async {
              final picked = await showDatePicker(
                context: context,
                initialDate: currentValue ?? DateTime.now(),
                firstDate: DateTime(2020),
                lastDate: DateTime.now(),
              );
              if (picked != null) {
                _updateFilter(filter.label, picked);
              }
            },
          ),
        ],
      ),
    );
  }

  Widget _buildCheckboxFilter(FilterConfig filter, ThemeData theme) {
    final isChecked = _currentFilters[filter.label] ?? false;

    return CheckboxListTile(
      title: Text(filter.label, style: theme.textTheme.bodyMedium),
      value: isChecked,
      onChanged: (value) => _updateFilter(filter.label, value ?? false),
      controlAffinity: ListTileControlAffinity.leading,
      contentPadding: const EdgeInsets.symmetric(horizontal: 8),
      visualDensity: VisualDensity.compact,
    );
  }

  Widget _buildMultiselectFilter(
    FilterConfig filter,
    ThemeData theme,
    double width,
  ) {
    final selectedValues = _currentFilters[filter.label] as List<String>? ?? [];

    return SizedBox(
      width: width,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            filter.label,
            style: theme.textTheme.bodySmall?.copyWith(
              fontWeight: FontWeight.w500,
              color: AppTheme.textSecondary,
            ),
          ),
          const SizedBox(height: 6),
          OutlinedButton.icon(
            onPressed: () async {
              final selected = await showDialog<List<String>>(
                context: context,
                builder: (context) => _MultiselectDialog(
                  title: filter.label,
                  options: filter.options ?? [],
                  selectedValues: selectedValues,
                ),
              );
              if (selected != null) {
                _updateFilter(filter.label, selected);
              }
            },
            icon: const Icon(Icons.expand_more, size: 18),
            label: Text(
              selectedValues.isNotEmpty
                  ? '${selectedValues.length} selected'
                  : 'Select options',
              style: theme.textTheme.bodyMedium,
            ),
            style: OutlinedButton.styleFrom(
              side: BorderSide(
                color: AppTheme.borderColor.withValues(alpha: 0.3),
              ),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
              alignment: Alignment.centerLeft,
            ),
          ),
        ],
      ),
    );
  }
}

class _MultiselectDialog extends StatefulWidget {
  const _MultiselectDialog({
    required this.title,
    required this.options,
    required this.selectedValues,
  });

  final String title;
  final List<String> options;
  final List<String> selectedValues;

  @override
  State<_MultiselectDialog> createState() => _MultiselectDialogState();
}

class _MultiselectDialogState extends State<_MultiselectDialog> {
  late List<String> _selectedValues;

  @override
  void initState() {
    super.initState();
    _selectedValues = List.from(widget.selectedValues);
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(widget.title),
      content: SizedBox(
        width: double.maxFinite,
        child: ListView.builder(
          shrinkWrap: true,
          itemCount: widget.options.length,
          itemBuilder: (context, index) {
            final option = widget.options[index];
            final isSelected = _selectedValues.contains(option);

            return CheckboxListTile(
              title: Text(option),
              value: isSelected,
              onChanged: (value) {
                setState(() {
                  if (value == true) {
                    _selectedValues.add(option);
                  } else {
                    _selectedValues.remove(option);
                  }
                });
              },
              controlAffinity: ListTileControlAffinity.leading,
              contentPadding: const EdgeInsets.symmetric(horizontal: 8),
              visualDensity: VisualDensity.compact,
            );
          },
        ),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(),
          child: const Text('Cancel'),
        ),
        TextButton(
          onPressed: () => Navigator.of(context).pop(_selectedValues),
          child: Text(
            'Apply (${_selectedValues.length})',
            style: const TextStyle(
              color: AppTheme.primaryColor,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }
}
