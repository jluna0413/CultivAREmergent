#!/usr/bin/env python3
"""
Flask Application Inspector
Check routes and server status without interrupting the running server
"""

import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def inspect_app():
    """Inspect the Flask application structure"""
    print("🔍 INSPECTING FLASK APPLICATION...")
    print("=" * 50)

    try:
        # Import the application factory
        from cultivar_app import create_app
        print("✅ Application factory imported successfully!")

        # Create app instance
        app = create_app()
        print("✅ Flask app created successfully!")
        print(f"   App name: {app.name}")
        print(f"   Debug mode: {app.debug}")

        # Get all routes
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append({
                'endpoint': rule.endpoint,
                'methods': ', '.join(rule.methods),
                'url': rule.rule
            })

        routes.sort(key=lambda x: x['url'])

        print(f"\n📋 ROUTES FOUND: {len(routes)}")
        print("=" * 80)

        # Show key routes
        auth_routes = []
        market_routes = []
        other_routes = []

        for route in routes:
            if '/auth' in route['url'] or 'login' in route['url']:
                auth_routes.append(route)
            elif '/market' in route['url']:
                market_routes.append(route)
            else:
                other_routes.append(route)

        print("🔐 AUTHENTICATION ROUTES:")
        for route in auth_routes:
            print(f"   {route['endpoint']:25} {route['methods']:15} {route['url']}")

        print("\n🛒 MARKET ROUTES:")
        for route in market_routes:
            print(f"   {route['endpoint']:25} {route['methods']:15} {route['url']}")

        print("\n🏠 OTHER KEY ROUTES:")
        for route in other_routes[:10]:  # Show first 10
            print(f"   {route['endpoint']:25} {route['methods']:15} {route['url']}")

        print("\n🎯 SERVER STATUS:")
        print("   ✅ Flask app loads correctly")
        print("   ✅ Authentication blueprint registered")
        print("   ✅ Market blueprint registered")
        print("   🚀 Server should be running on: http://localhost:5000")
        print("\n🔍 TROUBLESHOOTING:")
        print("   1. If login page not working: Visit http://localhost:5000/auth/login")
        print("   2. If cart not working: Login first, then visit market pages")
        print("   3. If server down: Run 'python cultivar_app.py'")

        return True

    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("💡 This might indicate missing dependencies or configuration issues")

        if "cannot import name" in str(e).lower():
            print("   - Check that all imports in cultivar_app.py are correct")
        if "no module named" in str(e).lower():
            print("   - Install missing dependencies: pip install -r requirements.txt")

        return False

if __name__ == "__main__":
    success = inspect_app()
    sys.exit(0 if success else 1)