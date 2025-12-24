import 'package:flutter/material.dart';

class CultivarDetailScreen extends StatelessWidget {
  const CultivarDetailScreen({super.key, required this.cultivarId});

  final String cultivarId;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Cultivar $cultivarId')),
      body: Center(child: Text('Cultivar Detail Screen for $cultivarId')),
    );
  }
}
