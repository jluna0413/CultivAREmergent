from flask import Flask, request # Import request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Minimal Flask Test!'

@app.route('/testpost', methods=['POST']) # New route for POST only
def test_post_route():
    return 'Minimal Flask Test POST OK'

if __name__ == '__main__':
    print("Starting minimal_flask_test.py on port 4200...")
    app.run(host='0.0.0.0', port=4200, debug=True, use_reloader=False)
