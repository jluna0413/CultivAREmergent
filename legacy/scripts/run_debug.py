import os
import sys

# Ensure repo root is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cultivar_app import create_app

app = create_app()

if __name__ == '__main__':
    # Force Flask debug mode for verbose tracebacks during local debugging
    port = int(os.getenv('CULTIVAR_PORT', 5000))
    print('Starting debug server on port', port)
    # Use the app's configured DEBUG value; allow overriding with FORCE_DEBUG env var for ad-hoc local debug
    force_debug = os.getenv('FORCE_DEBUG', '').lower() in ('1', 'true', 'yes')
    debug_flag = app.config.get('DEBUG', False) or force_debug
    app.run(host='127.0.0.1', port=port, debug=debug_flag, use_reloader=False)