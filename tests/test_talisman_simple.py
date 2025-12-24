#!/usr/bin/env python3
"""
Simple test to verify Flask-Talisman configuration without the full application.
"""

from flask import Flask
from flask_talisman import Talisman
import requests
import threading
import time
import sys

def test_talisman_configuration():
    """Test Flask-Talisman directly without database dependencies."""

    print("Testing Flask-Talisman configuration...")

    # Create a minimal Flask app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'test_key'
    app.config['DEBUG'] = True

    @app.route('/')
    def hello():
        return 'Hello, World!'

    # Configure Flask session settings
    app.config['SESSION_COOKIE_SECURE'] = False  # Debug mode
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    # Configure Flask-Talisman
    talisman = Talisman(
        app,
        content_security_policy={
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
            'style-src': "'self' 'unsafe-inline'",
            'img-src': "'self' data: https:",
            'font-src': "'self'",
            'connect-src': "'self'",
            'frame-src': "'none'",
            'object-src': "'none'",
            'base-uri': "'self'",
            'form-action': "'self'",
        },
        content_security_policy_nonce_in=['script-src', 'style-src'],
        strict_transport_security=False,  # Disabled for debug
        strict_transport_security_max_age=31536000,
        strict_transport_security_include_subdomains=False,
        strict_transport_security_preload=False,
        session_cookie_secure=False,  # Disabled for debug
        session_cookie_http_only=True,
        force_https=False,  # Disabled for debug
        force_https_permanent=False,
        force_file_save=False,
        frame_options='DENY',
        x_content_type_options='nosniff',
        referrer_policy='strict-origin-when-cross-origin',
        permissions_policy={
            'geolocation': (),
            'camera': (),
            'microphone': (),
            'payment': (),
            'usb': (),
        }
    )

    # Test with Flask test client
    with app.test_client() as client:
        response = client.get('/')
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")

        headers = dict(response.headers)
        for header in headers:
            print(f"  {header}: {headers[header]}")

        # Check key headers
        expected_headers = [
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Content-Security-Policy',
            'Referrer-Policy',
            'Permissions-Policy'
        ]

        missing_headers = []
        for header in expected_headers:
            if header not in headers:
                missing_headers.append(header)

        if missing_headers:
            print("\n❌ Missing security headers:")
            for header in missing_headers:
                print(f"   - {header}")
        else:
            print("\n✅ All key security headers are present!")

        # Check specific values
        print("\nValidation:")
        if headers.get('X-Frame-Options') == 'DENY':
            print("✅ X-Frame-Options: Correctly set to DENY")
        else:
            print(f"❌ X-Frame-Options: Expected 'DENY', got '{headers.get('X-Frame-Options')}'")

        if headers.get('X-Content-Type-Options') == 'nosniff':
            print("✅ X-Content-Type-Options: Correctly set to nosniff")
        else:
            print(f"❌ X-Content-Type-Options: Expected 'nosniff', got '{headers.get('X-Content-Type-Options')}'")

        if headers.get('Content-Security-Policy'):
            csp = headers.get('Content-Security-Policy')
            if 'default-src' in csp and "'self'" in csp:
                print("✅ Content-Security-Policy: Properly configured")
            else:
                print(f"❌ Content-Security-Policy: May be misconfigured: {csp[:100]}...")
        else:
            print("❌ Content-Security-Policy: Missing")

if __name__ == "__main__":
    test_talisman_configuration()