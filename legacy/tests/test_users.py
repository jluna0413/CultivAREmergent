import pytest
from cultivar_app import create_app
from app.models import db
from app.models.base_models import User
from werkzeug.security import check_password_hash

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
        # Create a user
        user = User(username='testuser', email='test@example.com', is_admin=False)
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

        yield testing_client

        db.drop_all()

def test_password_update(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN a user's password is updated
    THEN check that the password has been updated correctly
    """
    with test_client.application.app_context():
        user = User.query.filter_by(username='testuser').first()
        assert user is not None

        # Update password
        user.set_password('newpassword')
        db.session.commit()

        # Verify password
        assert check_password_hash(user.password_hash, 'newpassword')
