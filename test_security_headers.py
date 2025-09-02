#!/usr/bin/env python3
"""
Test script to verify Flask-Talisman security headers implementation.
"""

import requests
import time
import subprocess
import signal
import sys
import os

def test_security_headers():
    """Test that security headers are properly set in responses."""

    print("Testing Flask-Talisman security headers implementation...")

    # Start the Flask application in the background
    print("Starting CultivAR Flask application...")
    try:
        # Set environment variable for debug mode
        env = os.environ.copy()
        env['DEBUG'] = 'True'

        process = subprocess.Popen(
            [sys.executable, 'cultivar_app.py'],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for the app to start
        time.sleep(3)

        # Test HTTP response headers
        try:
            response = requests.get('http://localhost:5000/', timeout=10)
            print(f"Response Status Code: {response.status_code}")
            print("\nSecurity Headers:")

            security_headers = {
                'X-Frame-Options': response.headers.get('X-Frame-Options'),
                'X-Content-Type-Options': response.headers.get('X-Content-Type-Options'),
                'Content-Security-Policy': response.headers.get('Content-Security-Policy'),
                'X-XSS-Protection': response.headers.get('X-XSS-Protection'),
                'Referrer-Policy': response.headers.get('Referrer-Policy'),
                'Permissions-Policy': response.headers.get('Permissions-Policy'),
                'Strict-Transport-Security': response.headers.get('Strict-Transport-Security')
            }

            # Check development mode headers (HSTS should be missing in debug mode)
            for header, value in security_headers.items():
                if header == 'Strict-Transport-Security':
                    if value is None:
                        print(f"✅ {header}: Not set (expected in development mode)")
                    else:
                        print(f"❌ {header}: {value} (should not be set in development)")
                elif value is not None:
                    print(f"✅ {header}: {value}")
                else:
                    print(f"❌ {header}: Missing")

            print("\n" + "="*60)

            # Expected headers for development mode
            expected_headers = [
                ('X-Frame-Options', 'DENY'),
                ('X-Content-Type-Options', 'nosniff'),
                ('Content-Security-Policy', lambda v: v and 'default-src' in v),
                ('Referrer-Policy', 'strict-origin-when-cross-origin'),
                ('Permissions-Policy', lambda v: v and 'geolocation' in v),
                ('Strict-Transport-Security', None)  # Should be None in debug mode
            ]

            all_good = True
            for header_name, expected_value in expected_headers:
                actual_value = security_headers.get(header_name)
                if callable(expected_value):
                    if not expected_value(actual_value):
                        print(f"❌ {header_name}: Value doesn't match expected pattern")
                        all_good = False
                elif actual_value != expected_value:
                    print(f"❌ {header_name}: Expected '{expected_value}', got '{actual_value}'")
                    all_good = False

            if all_good:
                print("🎉 All security headers are properly configured!")
            else:
                print("⚠️  Some security headers may need attention.")

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to connect to the application: {e}")
            print("Make sure the Flask app is running and accessible.")

    except Exception as e:
        print(f"❌ Error starting Flask application: {e}")

    finally:
        # Clean up: terminate the Flask process
        try:
            if 'process' in locals():
                process.terminate()
                process.wait(timeout=5)
                print("\n🛑 Flask application stopped.")
        except Exception as e:
            print(f"⚠️  Error stopping Flask application: {e}")

if __name__ == "__main__":
    test_security_headers()