from flask import Flask
from flask_talisman import Talisman

app = Flask(__name__)
Talisman(app, x_xss_protection='1; mode=block')

@app.route('/')
def index():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(port=5001)
