"""
Main application file for the CultivAR application.
This is the entry point for the application.
"""

try:
    from flask import Flask, request
    print("Flask imported successfully")
except ImportError as e:
    print(f"Error importing Flask: {e}")
    print("Please install Flask: pip install flask")
    import sys # Import sys only if needed for sys.exit
    sys.exit(1)

# --- Minimal Flask App Definition ---
app = Flask(__name__)

@app.route('/')
def minimal_index():
    return "Minimal App Index OK - Main.py"

@app.route('/testlogin', methods=['POST']) # Changed to only accept POST
def test_login_route():
    # No longer checking request.method, as this route only handles POST
    return "Test Login POST-only OK - Main.py"
# --- End of Minimal Flask App Definition ---

if __name__ == '__main__':
    try:
        port = 5000 # Hardcoded port
        print(f"Starting Ultra-Minimal main.py Test App on port {port}...")
        print(f"Minimal application object created, attempting to run on port {port}...")
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error starting application: {e}")
