#!/usr/bin/env python3
"""
Debug script to check if market routes are properly registered.
Run this to see current route mapping and identify 404 issues.
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def debug_market_routes():
    """Debug market route registration issues."""
    from cultivar_app import create_app

    print("🔍 CULTIVAR MARKET ROUTES DEBUG")
    print("=" * 50)

    try:
        app = create_app()

        with app.app_context():
            print("\n📋 REGISTERED ROUTES:")
            print("-" * 30)

            # Get all registered routes
            routes = []
            for rule in app.url_map.iter_rules():
                if 'market' in rule.rule:
                    routes.append({
                        'rule': rule.rule,
                        'endpoint': rule.endpoint,
                        'methods': list(rule.methods - {'HEAD', 'OPTIONS'})
                    })

            if not routes:
                print("❌ NO MARKET ROUTES FOUND!")
            else:
                print("✅ FOUND MARKET ROUTES:")

                # Display all market routes
                for route in sorted(routes, key=lambda x: x['rule']):
                    methods = ', '.join(route['methods'])
                    print(f"  {route['rule']} -> {route['endpoint']} [{methods}]")

            print("\n🔧 BLUEPRINT CHECKS:")
            print("-" * 30)

            # Check if market blueprint is registered
            market_blueprints = [name for name, blueprint in app.blueprints.items() if 'market' in name.lower()]
            if market_blueprints:
                print(f"✅ Market blueprints registered: {market_blueprints}")
            else:
                print("❌ NO MARKET BLUEPRINTS REGISTERED!")

            # Check all blueprints
            print("\n📦 ALL REGISTERED BLUEPRINTS:")
            print("-" * 30)
            for name, blueprint in app.blueprints.items():
                if hasattr(blueprint, 'deferred_functions'):
                    url_prefix = getattr(blueprint, 'url_prefix', 'None')
                    print(f"  {name} (prefix: {url_prefix})")

            print("\n🌐 TESTING MARKET ROUTE VISIBILITY:")
            print("-" * 40)

            # Test if we can match market routes
            test_urls = [
                '/market/seed-bank',
                '/market/extensions',
                '/market/gear',
                '/cart'
            ]

            for url in test_urls:
                try:
                    # Try to match the URL
                    matched_url = app.url_map.bind('localhost').match(url)
                    endpoint = matched_url[0]
                    print(f"  ✅ {url} -> {endpoint}")
                except Exception as e:
                    print(f"  ❌ {url} -> NOT FOUND ({str(e)[:50]}...)")

    except Exception as e:
        print(f"❌ ERROR CREATING APP: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    debug_market_routes()