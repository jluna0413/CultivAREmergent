## Contributing guidelines — CultivAREmergent

This project has a mixed codebase and includes a Flutter subproject under `flutter_app`.
Follow these lightweight rules to keep PRs reviewable and CI-friendly.

1. Logging
   - Use `flutter_app/lib/core/logging.dart`'s `AppLogger` wrapper for all runtime logs.
   - Avoid `print(...)` and `debugPrint(...)` in application code; prefer `AppLogger.log(...)` or
     `AppLogger.error(...)` so we can add structured logging later without touching many files.

2. Lint & Analyzer
   - A GitHub Actions workflow runs `flutter analyze` (and `flutter test` where available) for the
     Flutter app on PRs. Fix analyzer warnings before requesting review.

3. Tests
   - Add small, focused unit tests for new logic. Tests live in `flutter_app/test` and can be run
     locally with `flutter test` from the `flutter_app` folder.

4. PRs
   - Keep PRs small and focused: one logical change per PR (formatting / linting can be batched).
   - Use descriptive commit messages and include a short testing checklist in the PR body.

5. Builds
   - The repository may not contain the Flutter `pubspec.yaml` at the top-level. When adding or
     editing dependencies, update `flutter_app/pubspec.yaml` and run `flutter pub get` before
     pushing.

If anything in these rules isn't feasible for your change, mention it in the PR and reviewers
will help triage.
