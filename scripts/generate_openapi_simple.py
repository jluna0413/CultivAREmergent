#!/usr/bin/env python3
"""
Simple OpenAPI spec generator to avoid environment variable issues
"""
import os
import sys
import json

# Set environment variable before importing app
os.environ['SECRET_KEY'] = 'test-secret-key-for-openapi-generation'
# Don't skip routers - we want them loaded for the OpenAPI spec
# os.environ['FASTAPI_SKIP_ROUTERS'] = '1'  # Skip router imports to avoid other issues

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from app.fastapi_app import app
    from fastapi.openapi.utils import get_openapi
    
    # Generate OpenAPI schema
    openapi_schema = get_openapi(
        title="Cultivar Collection Management API",
        version="2.0.0",
        routes=app.routes,
    )
    
    # Ensure directory exists
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'docs', 'generated')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save to file
    output_file = os.path.join(output_dir, 'openapi.json')
    with open(output_file, 'w') as f:
        json.dump(openapi_schema, f, indent=2)
    
    print(f"OpenAPI spec generated successfully!")
    print(f"Output file: {output_file}")
    print(f"Primary endpoint: /api/v1/cultivars")
    print(f"Legacy endpoint: /api/v1/strains")
    
    # Check if cultivars endpoints are present
    paths = openapi_schema.get('paths', {})
    cultivars_paths = [path for path in paths.keys() if '/api/v1/cultivars' in path]
    strains_paths = [path for path in paths.keys() if '/api/v1/strains' in path]
    
    print(f"Found {len(cultivars_paths)} cultivars endpoints")
    print(f"Found {len(strains_paths)} legacy strains endpoints")
    
    for path in cultivars_paths[:3]:  # Show first 3
        print(f"  - {path}")
    
    if strains_paths:
        for path in strains_paths[:3]:  # Show first 3
            print(f"  - {path} (legacy)")
    
except Exception as e:
    print(f"Error generating OpenAPI spec: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)