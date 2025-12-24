import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class GeneticsSlider extends StatefulWidget {
  final int indicaPercentage;
  final int sativaPercentage;
  final ValueChanged<int> onIndicaChanged;
  final ValueChanged<int> onSativaChanged;

  const GeneticsSlider({
    super.key,
    required this.indicaPercentage,
    required this.sativaPercentage,
    required this.onIndicaChanged,
    required this.onSativaChanged,
  });

  @override
  State<GeneticsSlider> createState() => _GeneticsSliderState();
}

class _GeneticsSliderState extends State<GeneticsSlider> {
  late int _indica;
  late int _sativa;

  @override
  void initState() {
    super.initState();
    _indica = widget.indicaPercentage;
    _sativa = widget.sativaPercentage;
  }

  @override
  void didUpdateWidget(GeneticsSlider oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.indicaPercentage != widget.indicaPercentage ||
        oldWidget.sativaPercentage != widget.sativaPercentage) {
      _indica = widget.indicaPercentage;
      _sativa = widget.sativaPercentage;
    }
  }

  void _updateIndica(double value) {
    final newIndica = value.round();
    final newSativa = 100 - newIndica;

    setState(() {
      _indica = newIndica;
      _sativa = newSativa;
    });

    widget.onIndicaChanged(newIndica);
    widget.onSativaChanged(newSativa);
  }

  void _updateSativa(double value) {
    final newSativa = value.round();
    final newIndica = 100 - newSativa;

    setState(() {
      _indica = newIndica;
      _sativa = newSativa;
    });

    widget.onIndicaChanged(newIndica);
    widget.onSativaChanged(newSativa);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Genetics',
          style: TextStyle(
            color: Colors.white,
            fontSize: 16,
            fontWeight: FontWeight.w500,
          ),
        ),
        const SizedBox(height: 16),

        // Percentage inputs
        Row(
          children: [
            Expanded(
              child: Column(
                children: [
                  Text(
                    'Indica',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.7),
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF3a3a3a),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white24),
                    ),
                    child: Text(
                      '$_indica%',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Column(
                children: [
                  Text(
                    'Sativa',
                    style: TextStyle(
                      color: Colors.white.withOpacity(0.7),
                      fontSize: 14,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 16,
                      vertical: 12,
                    ),
                    decoration: BoxDecoration(
                      color: const Color(0xFF3a3a3a),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.white24),
                    ),
                    child: Text(
                      '$_sativa%',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),

        const SizedBox(height: 16),

        // Slider
        SliderTheme(
          data: SliderThemeData(
            activeTrackColor: AppColors.primary500,
            inactiveTrackColor: Colors.white24,
            thumbColor: AppColors.primary500,
            overlayColor: AppColors.primary500.withOpacity(0.2),
            trackHeight: 8,
            thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 12),
            overlayShape: const RoundSliderOverlayShape(overlayRadius: 20),
          ),
          child: Slider(
            value: _indica.toDouble(),
            min: 0,
            max: 100,
            divisions: 100,
            onChanged: _updateIndica,
          ),
        ),

        const SizedBox(height: 8),

        // Labels
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              'Indica Dominant',
              style: TextStyle(
                color: Colors.white.withOpacity(0.6),
                fontSize: 12,
              ),
            ),
            Text(
              'Sativa Dominant',
              style: TextStyle(
                color: Colors.white.withOpacity(0.6),
                fontSize: 12,
              ),
            ),
          ],
        ),

        const SizedBox(height: 8),

        // Visual representation
        Container(
          height: 12,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(6),
            color: Colors.white12,
          ),
          child: Row(
            children: [
              Expanded(
                flex: _indica,
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: _indica == 100
                        ? BorderRadius.circular(6)
                        : const BorderRadius.only(
                            topLeft: Radius.circular(6),
                            bottomLeft: Radius.circular(6),
                          ),
                    color: AppColors.primary500.withOpacity(0.6),
                  ),
                ),
              ),
              Expanded(
                flex: _sativa,
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: _sativa == 100
                        ? BorderRadius.circular(6)
                        : const BorderRadius.only(
                            topRight: Radius.circular(6),
                            bottomRight: Radius.circular(6),
                          ),
                    color: Colors.orange.withOpacity(0.6),
                  ),
                ),
              ),
            ],
          ),
        ),

        const SizedBox(height: 8),

        // Legend
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Row(
              children: [
                Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(2),
                    color: AppColors.primary500.withOpacity(0.6),
                  ),
                ),
                const SizedBox(width: 4),
                Text(
                  'Indica',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.7),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
            const SizedBox(width: 16),
            Row(
              children: [
                Container(
                  width: 12,
                  height: 12,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(2),
                    color: Colors.orange.withOpacity(0.6),
                  ),
                ),
                const SizedBox(width: 4),
                Text(
                  'Sativa',
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.7),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }
}
