import pytest
from cultivar_app import create_app

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
        yield testing_client

def test_security_headers(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested
    THEN check that the security headers are set correctly
    """
    response = test_client.get('/')
    headers = response.headers

    assert headers['X-Frame-Options'] == 'DENY'
    assert headers['X-Content-Type-Options'] == 'nosniff'
    assert 'default-src' in headers['Content-Security-Policy']
    assert headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'
    assert 'geolocation' in headers['Permissions-Policy']
    assert 'Strict-Transport-Security' not in headers # Should not be set in debug mode
