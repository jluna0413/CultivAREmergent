#!/usr/bin/env python3
"""
Simple test script to verify Flask application is working
"""

import sys
import os
import requests

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

try:
    from cultivar_app import create_app

    print("🧪 Testing Flask Application...")
    print("=" * 50)

    # Create app instance
    app = create_app()

    with app.app_context():
        print("✅ Flask app created successfully")

        # Test static file access
        from flask import url_for
        try:
            css_url = url_for('static', filename='css/styles.css')
            print(f"✅ CSS URL generated: {css_url}")

            js_url = url_for('static', filename='js/theme-manager.js')
            print(f"✅ JS URL generated: {js_url}")
        except Exception as e:
            print(f"❌ Static URL generation failed: {e}")

        # Test template rendering
        try:
            from flask import render_template
            rendered = render_template('landing/index.html')
            if 'CultivAR' in rendered:
                print("✅ Template rendered successfully")
                print(f"📏 Template size: {len(rendered)} characters")

                # Check if our new CSS class exists
                if 'theme-toggle-fixed' in rendered:
                    print("✅ Design system classes found in template")
                else:
                    print("❌ Design system classes NOT found in template")

                # Check for script loading
                if 'theme-manager.js' in rendered:
                    print("✅ Theme manager script referenced")
                else:
                    print("❌ Theme manager script NOT found")

            else:
                print("❌ Template rendering failed")
        except Exception as e:
            print(f"❌ Template rendering error: {e}")

    print("\n" + "=" * 50)
    print("🚀 Flask app should be running at http://localhost:5000")

except Exception as e:
    print(f"❌ Flask app creation failed: {e}")
    import traceback
    traceback.print_exc()
