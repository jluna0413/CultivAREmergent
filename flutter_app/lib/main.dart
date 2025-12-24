import 'package:flutter/material.dart';
import 'package:cultivar_app/core/providers/riverpod_exports.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:cultivar_app/config/router/app_router.dart' as router;
import 'package:cultivar_app/core/theme/app_theme.dart';

Future<void> main() async {
  try {
    WidgetsFlutterBinding.ensureInitialized();
    print('DEBUG: App initialization started');

    await dotenv.load();
    print('DEBUG: Environment loaded');

    FlutterError.onError = (FlutterErrorDetails details) {
      print('FLUTTER ERROR: ${details.exception}');
      print('STACK: ${details.stack}');
    };

    runApp(const ProviderScope(child: MyApp()));
    debugPrint('DEBUG: runApp called');
  } catch (e, stack) {
    debugPrint('FATAL ERROR in main: $e');
    debugPrint(stack.toString());
    // Try to run a simple error app
    runApp(
      Directionality(
        textDirection: TextDirection.ltr,
        child: Container(
          color: const Color(0xFFFF0000),
          child: Center(
            child: Text(
              'FATAL ERROR:\n$e',
              style: const TextStyle(color: Color(0xFFFFFFFF), fontSize: 24),
            ),
          ),
        ),
      ),
    );
  }
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    debugPrint('DEBUG: MyApp building');
    final goRouter = ref.watch(router.goRouterProvider);
    debugPrint('DEBUG: GoRouter obtained');

    return MaterialApp.router(
      title: 'CultivAR',
      theme: lightTheme,
      darkTheme: darkTheme,
      routerConfig: goRouter,
    );
  }
}
