// Placeholder for login screen UI
import 'package:flutter/material.dart';
import '../../../core/providers/riverpod_exports.dart';

import '../../../core/state/auth_provider.dart';
import '../../../core/widgets/custom_button.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [Color(0xFF1a1a1a), Color(0xFF2d2d2d)],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24.0),
            child: Container(
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: Colors.white24),
              ),
              child: Padding(
                padding: const EdgeInsets.all(32.0),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      'CultivAR',
                      style: TextStyle(
                        color: Color(0xFF4CAF50),
                        fontSize: 36,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    const SizedBox(height: 8),
                    const Text(
                      'Cannabis Grow Journal',
                      style: TextStyle(color: Colors.white70, fontSize: 16),
                    ),
                    const SizedBox(height: 48),

                    // OIDC Login Button
                    if (authState.isLoading)
                      const CircularProgressIndicator()
                    else
                      CustomButton(
                        onPressed: () {
                          ref.read(authProvider.notifier).login();
                        },
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.login),
                            SizedBox(width: 8),
                            Text('Login with CultivAR ID'),
                          ],
                        ),
                      ),

                    const SizedBox(height: 24),
                    // Optional: Dev Login for debug builds if needed
                    // But for now keeping it clean.
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
