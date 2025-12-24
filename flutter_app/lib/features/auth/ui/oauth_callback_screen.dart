// OAuth Callback Screen - handles authorization code exchange
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../../core/auth/oauth_repository.dart';

class OAuthCallbackScreen extends ConsumerStatefulWidget {
  final String? code;
  final String? state;
  final String? error;
  final String? errorDescription;

  const OAuthCallbackScreen({
    super.key,
    this.code,
    this.state,
    this.error,
    this.errorDescription,
  });

  @override
  ConsumerState<OAuthCallbackScreen> createState() =>
      _OAuthCallbackScreenState();
}

class _OAuthCallbackScreenState extends ConsumerState<OAuthCallbackScreen> {
  bool _isProcessing = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _processCallback();
  }

  Future<void> _processCallback() async {
    // Check for errors from Keycloak
    if (widget.error != null) {
      setState(() {
        _isProcessing = false;
        _errorMessage =
            widget.errorDescription ?? 'Authentication failed: ${widget.error}';
      });
      return;
    }

    // Check for authorization code
    if (widget.code == null) {
      setState(() {
        _isProcessing = false;
        _errorMessage = 'No authorization code received';
      });
      return;
    }

    // Exchange code for tokens
    final success = await getOAuthRepository().handleCallback(
      widget.code!,
      widget.state,
    );

    if (success) {
      // Reload user in auth state
      final user = await getOAuthRepository().getCurrentUser();
      if (user != null && mounted) {
        // Navigate to dashboard
        context.go('/dashboard');
      } else {
        setState(() {
          _isProcessing = false;
          _errorMessage = 'Failed to load user profile';
        });
      }
    } else {
      setState(() {
        _isProcessing = false;
        _errorMessage = 'Token exchange failed';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isProcessing) {
      return const Scaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              CircularProgressIndicator(),
              SizedBox(height: 24),
              Text('Completing login...', style: TextStyle(fontSize: 18)),
              SizedBox(height: 8),
              Text(
                'Please wait while we verify your credentials',
                style: TextStyle(color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    // Error state
    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline, size: 64, color: Colors.red),
              const SizedBox(height: 24),
              const Text(
                'Login Failed',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Text(
                _errorMessage ?? 'An unknown error occurred',
                textAlign: TextAlign.center,
                style: const TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 32),
              ElevatedButton(
                onPressed: () => context.go('/login'),
                child: const Text('Try Again'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
