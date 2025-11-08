#!/usr/bin/env python3
"""
Script to generate OpenAPI schema snapshot for CI/CD pipeline
"""
import json
import os
import sys

# Add the app directory to the Python path
sys.path.insert(0, '.')

try:
    from app.fastapi_app import app
    from fastapi.testclient import TestClient
    
    print('✅ Successfully imported FastAPI app')
    
    # Create test client and generate OpenAPI schema
    print(app.user_middleware)
    client = TestClient(app, base_url="http://testserver")
    response = client.get('/openapi.json', headers={"Host": "testserver"})
    
    if response.status_code == 200:
        schema = response.json()
        
        # Ensure directory exists
        os.makedirs('docs/generated', exist_ok=True)
        
        # Write OpenAPI schema to file
        with open('docs/generated/openapi.json', 'w') as f:
            json.dump(schema, f, indent=2)
        
        print('✅ OpenAPI schema generated successfully!')
        print(f'📁 Saved to: docs/generated/openapi.json')
        print(f'📊 Schema info: {schema.get("info", {}).get("title", "Unknown")} v{schema.get("info", {}).get("version", "Unknown")}')
        print(f'🔗 Paths defined: {len(schema.get("paths", {}))} endpoints')
        print(f'📚 Components: {len(schema.get("components", {}).get("schemas", {}))} schemas')
    else:
        print(f'❌ Failed to generate OpenAPI schema: {response.status_code}')
        print(f'Response: {response.text}')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ Error: {e}')
    import traceback
    traceback.print_exc()
    sys.exit(1)
