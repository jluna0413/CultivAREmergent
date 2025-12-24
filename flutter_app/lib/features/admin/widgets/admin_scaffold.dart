import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

class AdminScaffold extends ConsumerStatefulWidget {
  const AdminScaffold({
    super.key,
    required this.body,
    this.title,
    this.actions,
    this.floatingActionButton,
  });

  final Widget body;
  final String? title;
  final List<Widget>? actions;
  final Widget? floatingActionButton;

  @override
  ConsumerState<AdminScaffold> createState() => _AdminScaffoldState();
}

class _AdminScaffoldState extends ConsumerState<AdminScaffold> {
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () => _scaffoldKey.currentState?.openDrawer(),
          tooltip: 'Open Menu',
        ),
        title: Text(widget.title ?? 'Admin Panel'),
        actions: [...?widget.actions],
        backgroundColor: Theme.of(context).primaryColor,
        elevation: 2,
      ),
      drawer: Drawer(
        child: ListView(
          padding: EdgeInsets.zero,
          children: [
            DrawerHeader(
              decoration: BoxDecoration(color: Theme.of(context).primaryColor),
              child: const Text(
                'Admin Panel',
                style: TextStyle(color: Colors.white, fontSize: 24),
              ),
            ),
            ListTile(
              leading: const Icon(Icons.dashboard),
              title: const Text('Dashboard'),
              onTap: () {
                Navigator.of(context).pop();
                // TODO: Navigate to dashboard
              },
            ),
            ListTile(
              leading: const Icon(Icons.people),
              title: const Text('Users'),
              onTap: () {
                Navigator.of(context).pop();
                // TODO: Navigate to users
              },
            ),
            ListTile(
              leading: const Icon(Icons.psychology),
              title: const Text('Agent Hub'),
              onTap: () {
                Navigator.of(context).pop();
                context.goNamed('agent-hub');
              },
            ),
            const Divider(),
            ListTile(
              leading: const Icon(Icons.settings),
              title: const Text('Settings'),
              onTap: () {
                Navigator.of(context).pop();
                // TODO: Navigate to settings
              },
            ),
          ],
        ),
      ),
      body: widget.body,
      floatingActionButton: widget.floatingActionButton,
    );
  }
}

// AGENT_SIGNATURE: (Agent Type: IDE, Name: Kilo-Code, Action: Fix)
