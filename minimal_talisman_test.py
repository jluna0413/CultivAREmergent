#!/usr/bin/env python3
"""
Minimal test to verify Flask-Talisman is working.
"""

from flask import Flask
from flask_talisman import Talisman
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_key'
app.config['DEBUG'] = True

# Configure Flask session settings
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

@app.route('/')
def hello():
    return 'Hello from Flask-Talisman Test!'

# Configure Flask-Talisman with minimal, safe settings
talisman = Talisman(
    app,
    frame_options='DENY',
    content_security_policy={
        'default-src': "'self'"
    },
    x_content_type_options='nosniff',
    referrer_policy='strict-origin-when-cross-origin'
)

if __name__ == '__main__':
    with app.test_client() as client:
        response = client.get('/')
        print(f"Status: {response.status_code}")
        print("Response headers:")
        for name, value in response.headers:
            if any(keyword in name.lower() for keyword in ['x-frame', 'x-content', 'content-sec', 'referrer', 'strict']):
                print(f"  {name}: {value}")

        print("\nChecking specific headers:")
        frame_options = response.headers.get('X-Frame-Options')
        content_type = response.headers.get('X-Content-Type-Options')
        referrer = response.headers.get('Referrer-Policy')

        print(f"X-Frame-Options: {frame_options} (expected: DENY)")
        print(f"X-Content-Type-Options: {content_type} (expected: nosniff)")
        print(f"Referrer-Policy: {referrer} (expected: strict-origin-when-cross-origin)")

    print("\nMinimal Talisman test completed.")