import json
from pathlib import Path
import pytest
from app import create_app, db
from config import TestConfig

app = create_app(TestConfig)

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        # db.drop_all()

def login(client, username, password):
    """Login helper function"""
    return client.post(
        "/login",
        data=dict(username=username, password=password),
        follow_redirects=True,
    )

def logout(client):
    """Logout helper function"""
    return client.get("/logout", follow_redirects=True)

def test_login_logout(client):
    """Test login and logout using helper functions"""
    rv = login(client, app.config.get("USERNAME"), app.config.get("PASSWORD"))
    assert rv.status_code == 200
    rv = logout(client)
    assert rv.status_code == 200