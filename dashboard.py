from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
import os
from app.models import db, migrate_db, init_db
from app.handlers import plant_handlers, strain_handlers, sensor_handlers
from app.config import Config
from app.config.load_config import load_config_from_db

app = Flask(__name__,
            template_folder='app/web/templates',
            static_folder='app/web/static')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_key')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

base_dir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(base_dir, 'data')
os.makedirs(data_dir, exist_ok=True)

db_path = os.path.join(data_dir, 'cultivar.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)

with app.app_context():
    migrate_db()
    init_db()
    load_config_from_db()

@app.route('/')
def dashboard():
    plants = plant_handlers.get_living_plants()
    strains = len(Config.Strains) if hasattr(Config, 'Strains') else 0
    sensors = sensor_handlers.get_sensors()
    sensors_count = len(sensors) if sensors else 0
    harvests = plant_handlers.get_harvested_plants()
    harvests_count = len(harvests) if harvests else 0

    return render_template('views/index.html',
                          title='Dashboard',
                          plants=plants,
                          strains=strains,
                          sensors=sensors_count,
                          harvests=harvests_count,
                          activities=Config.Activities)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    print('Starting CultivAR on port 5555...')
    app.run(host='0.0.0.0', port=5555, debug=True)
