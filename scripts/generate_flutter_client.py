#!/usr/bin/env python3
"""
Flutter Client Generator
Generates Dart/Flutter client from OpenAPI specification
"""

import json
import os
import sys
import subprocess
import argparse
from pathlib import Path

def generate_dart_client(openapi_path: str, output_dir: str) -> bool:
    """Generate Dart client using OpenAPI Generator CLI."""
    try:
        # Ensure output directory exists
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Check if OpenAPI generator CLI is available
        try:
            subprocess.run(["npx", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Node.js/npm not available. Skipping Dart client generation.")
            print("Install Node.js and run: npm install -g @openapitools/openapi-generator-cli")
            return False
        
        # Generate Dart client
        cmd = [
            "npx", "@openapitools/openapi-generator-cli", "generate",
            "-i", str(openapi_path),
            "-g", "dart",
            "-o", str(output_dir),
            "--package-name", "cultivar_api",
            "--model-package", "models",
            "--api-package", "api"
        ]
        
        print(f"Generating Flutter/Dart client...")
        print(f"Command: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Flutter client generated successfully in: {output_dir}")
            return True
        else:
            print(f"Error generating Flutter client: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False

def create_flutter_client_integration(output_dir: str) -> None:
    """Create Flutter client integration instructions."""
    integration_instructions = f"""
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
   cp -r {output_dir}/* your_flutter_app/lib/api/
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

## Generated: {Path(__file__).stat().st_mtime}
"""
    
    readme_path = Path(output_dir) / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(integration_instructions)
    
    print(f"Integration instructions saved to: {readme_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate Flutter client from OpenAPI spec")
    parser.add_argument(
        "--openapi-spec",
        default="docs/generated/openapi.json",
        help="Path to OpenAPI specification file"
    )
    parser.add_argument(
        "--output-dir",
        default="flutter_client_generated",
        help="Output directory for generated Flutter client"
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Skip client generation, only create integration docs"
    )
    
    args = parser.parse_args()
    
    print("Flutter Client Generator")
    print("=" * 50)
    
    openapi_path = Path(args.openapi_spec)
    if not openapi_path.exists():
        print(f"Error: OpenAPI spec not found: {openapi_path}")
        sys.exit(1)
    
    # Create integration instructions
    create_flutter_client_integration(args.output_dir)
    
    if not args.skip_generation:
        # Generate Dart client
        success = generate_dart_client(openapi_path, args.output_dir)
        
        if success:
            print(f"\n[SUCCESS] Flutter client generated successfully!")
            print(f"Output directory: {args.output_dir}")
        else:
            print(f"\n[WARNING] Flutter client generation failed or skipped.")
            print(f"Integration docs created: {args.output_dir}/README.md")
    else:
        print(f"\n[INFO] Client generation skipped. Integration docs created: {args.output_dir}/README.md")

if __name__ == "__main__":
    main()