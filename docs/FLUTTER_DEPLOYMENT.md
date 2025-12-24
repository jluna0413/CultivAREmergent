# Flutter Deployment Guide for CultivAR

## Web Deployment

1. Build release:
   ```
   flutter build web --release
   ```

2. Copy to backend static:
   ```
   cp -r build/web/* app/web/static/flutter/
   ```

3. FastAPI serve:
   - Route `/` serve `index.html`
   - Catch-all `*` serve `index.html` for SPA routing

## Android Deployment

1. Configure keystore `key.properties`:
   ```
   storePassword=***
   keyPassword=***
   keyAlias=***
   storeFile=***
   ```

2. Build APK:
   ```
   flutter build apk --release
   ```

3. Manifest permissions (android/app/src/main/AndroidManifest.xml):
   - INTERNET
   - CAMERA (image_picker)
   - STORAGE

4. Play Console:
   - Internal testing → Production rollout

## iOS Deployment

1. Build IPA:
   ```
   flutter build ipa --release
   ```

2. Xcode signing:
   - Bundle ID, provisioning profile
   - Info.plist: camera usage, network

3. App Store:
   - TestFlight beta → Production

## Version Management

- pubspec.yaml `version: 1.0.0+1`
- CHANGELOG.md semantic versioning

## Rollout Strategy

- Feature flags: flutter_firebase_remote_config
- Staged rollout: 10% → 50% → 100%
- Monitoring: Firebase Crashlytics, Sentry

## CI/CD - GitHub Actions

```yaml
name: Flutter CI/CD
on: [push, pull_request]
jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          channel: stable
      - run: flutter pub get
      - run: flutter analyze
      - run: flutter test --coverage
      - uses: codecov/codecov-action@v3
        with:
          file: coverage/lcov.info
          fail_ci_if_below_threshold: 80
  deploy-web:
    needs: build-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - run: flutter build web --release
      - uses: actions/upload-artifact@v3
        with:
          name: web-build
          path: build/web
  deploy-stores:
    needs: build-test
    runs-on: macos-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: flutter build apk --release
      - run: flutter build ipa --release
      # Fastlane or manual upload
```
