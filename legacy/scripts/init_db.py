# scripts/init_db.py
import click
from flask.cli import with_appcontext
from app.models import db, init_db
from app.models.base_models import Plant, Strain, Status, Zone, Breeder, User
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

@click.command('init-db')
@click.option('--demo', is_flag=True, help='Create demo data.')
@with_appcontext
def init_db_command(demo):
    """Clear the existing data and create new tables."""
    db.create_all()
    init_db()
    if demo:
        create_demo_data()
    click.echo('Initialized the database.')

def create_demo_data():
    """Create demo data for the application."""
    if User.query.filter_by(username='admin').first() is None:
        admin_user = User(
            username='admin',
            is_admin=True,
            password_hash=generate_password_hash('admin')
        )
        db.session.add(admin_user)

    if Plant.query.count() == 0:
        # Create a test breeder
        test_breeder = Breeder.query.filter_by(name='CultivAR Seeds').first()
        if not test_breeder:
            test_breeder = Breeder()
            test_breeder.name = 'CultivAR Seeds'
            db.session.add(test_breeder)
            db.session.flush()
        
        # Create a test strain
        test_strain = Strain.query.filter_by(name='Green Goddess').first()
        if not test_strain:
            test_strain = Strain(
                name='Green Goddess',
                breeder_id=test_breeder.id,
                indica=60,
                sativa=40,
                description='Premium hybrid strain perfect for cloning',
                seed_count=10,
                cycle_time=75
            )
            db.session.add(test_strain)
            db.session.flush()
        
        # Create a test zone
        test_zone = Zone.query.filter_by(name='Grow Tent 1').first()
        if not test_zone:
            test_zone = Zone(name='Grow Tent 1')
            db.session.add(test_zone)
            db.session.flush()
        
        # Create a test plant
        test_plant = Plant(
            name='Mother Plant Alpha',
            description='Healthy mother plant ready for cloning',
            strain_id=test_strain.id,
            zone_id=test_zone.id,
            status_id=2,  # Vegetative
            is_clone=False,
            start_dt=datetime.now() - timedelta(days=45),
            current_week=7,
            current_day=3
        )
        db.session.add(test_plant)
        db.session.commit()
        click.echo("Created test plant 'Mother Plant Alpha' for clone demonstration")

def register_commands(app):
    app.cli.add_command(init_db_command)
