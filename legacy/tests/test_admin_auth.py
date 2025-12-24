import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from cultivar_app import create_app
from app.models import db
from app.models.base_models import User
from flask_login import login_user

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.update({
        "TESTING": True,
        "DEBUG": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        # Create a non-admin user
        non_admin_user = User(username='testuser', email='test@example.com', is_admin=False)
        non_admin_user.set_password('password')
        db.session.add(non_admin_user)

        # Create an admin user
        admin_user = User(username='adminuser', email='admin@example.com', is_admin=True)
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)

        db.session.commit()

        yield testing_client

        db.drop_all()

def test_diagnostics_as_non_admin(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/diagnostics' page is requested by a non-admin user
    THEN check that a 403 status code is returned
    """
    with test_client.application.test_request_context():
        user = User.query.filter_by(username='testuser').first()
        login_user(user)
        response = test_client.get('/diagnostics')
        assert response.status_code == 403

def test_diagnostics_as_admin(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/diagnostics' page is requested by an admin user
    THEN check that a 200 status code is returned
    """
    with test_client.application.test_request_context():
        user = User.query.filter_by(username='adminuser').first()
        login_user(user)
        response = test_client.get('/diagnostics')
        assert response.status_code == 200

def test_admin_diagnostics_test_as_non_admin(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/api/diagnostics/test' page is requested by a non-admin user
    THEN check that a 403 status code is returned
    """
    with test_client.application.test_request_context():
        user = User.query.filter_by(username='testuser').first()
        login_user(user)
        response = test_client.get('/admin/api/diagnostics/test')
        assert response.status_code == 403

def test_admin_diagnostics_test_as_admin(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/admin/api/diagnostics/test' page is requested by an admin user
    THEN check that a 200 status code is returned
    """
    with test_client.application.test_request_context():
        user = User.query.filter_by(username='adminuser').first()
        login_user(user)
        response = test_client.get('/admin/api/diagnostics/test')
        assert response.status_code == 200
