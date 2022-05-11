import pytest
from app.db import db
from app.db.models import User


def test_menu_links(client):
    response = client.get("/")

    assert response.status_code == 200

    assert b'href="/about"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data
    #assert b'href="/map"' in response.data

def test_file_upload(client):
    statuscode = 404
    assert statuscode == client.get('locations/uploads').status_code == 404
    assert db.session.query(User).count() == 0


