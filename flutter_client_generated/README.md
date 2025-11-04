
# Flutter Client Integration

This directory contains the generated Flutter/Dart client for the CultivAR API.

## Generated Files

- `lib/api/` - API client classes
- `lib/model/` - Data model classes  
- `lib/api_client.dart` - Main API client
- `pubspec.yaml` - Required dependencies

## Setup Instructions

1. Copy the generated client to your Flutter project:
   ```bash
   cp -r flutter_client_generated/* your_flutter_app/lib/api/
   ```

2. Add required dependencies to pubspec.yaml:
   ```yaml
   dependencies:
     http: ^1.1.0
     dart_openapi_codegen:
       path: ./lib/api
   ```

3. Initialize the API client:
   ```dart
   import 'package:cultivar_api/api_client.dart';
   
   final apiClient = ApiClient();
   final plantsApi = PlantsApi(apiClient);
   ```

## Usage Example

```dart
// Get list of plants
final plants = await plantsApi.getPlants();
print(plants.map((p) => p.name).toList());
```

## API Documentation

Full API documentation is available at:
- OpenAPI Spec: docs/generated/openapi.json
- Interactive Docs: /docs (when API server is running)

## Generated: 1762026987.6263864
