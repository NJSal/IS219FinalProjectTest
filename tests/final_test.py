import sqlite3
from urllib import request
import os
import pytest
from app.db.models import User

from app import db, auth

from app.auth.forms import csv_upload
from flask_login import FlaskLoginClient

from flask_login import current_user

from app.db.models import User, Location

from app.db import db
from app import create_app

from flask import redirect, url_for, request
from http import HTTPStatus

from flask import session
from flask import g, logging

import app

import os
import logging

from click.testing import CliRunner

from app import create_database, create_log_folder

runner = CliRunner()

def test_menu_links(client):
    response = client.get("/")

    assert response.status_code == 200

    assert b'href="/about"' in response.data
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data
    #assert b'href="/map"' in response.data

def test_registration(client):
    response = client.post("/register", data={"email": "123@mail", "password": "123"}, follow_redirects=True)
    response.status_code == 302

def test_file_upload(client):
    statuscode = 404
    assert statuscode == client.get('locations/uploads').status_code == 404
    assert db.session.query(User).count() == 0

def test_database_creation():
    response = runner.invoke(create_database)
    exitcode = 0
    assert response.exit_code == exitcode

    location = os.path.dirname(os.path.abspath(__file__))
    directorylocation = '../database'

    dir = os.path.join(location, directorylocation)
    assert os.path.exists(dir) == True


def test_edit_location(application):
    application.test_client_class = FlaskLoginClient

    user = User('admi34n@adminemail.com', 'AdminName1', 1)
    location = Location("title", "longitude", "latitude", "population")
    db.session.add(user)

    reguser = User('admi2141@email.com', 'Amindasdasdm', 0)
    db.session.add(reguser)
    db.session.add(location)
    db.session.commit()

    assert db.session.query(User).count() == 2

    assert db.session.query(Location).count() == 1

    with application.test_client(user=user) as client:
        response = client.post('/locations/1/edit', data={"title": "tite", "population": "population"},
                              follow_redirects=True)
        assert b'Location Edited Successfully' in response.data

def test_upload_locations(application):
    application.test_client_class = FlaskLoginClient
    user = User('sample1@sample.com', 'testtest', 1)
    db.session.add(user)

    db.session.commit()

    assert user.email == 'sample1@sample.com'
    assert db.session.query(User).count() == 1

    root = os.path.dirname(os.path.abspath(__file__))

    directory = "../uploads/us_cities_short.csv"
    locations = os.path.join(root, directory)

    with application.test_client(user=user) as client:
        response = client.get('/locations/upload')

        assert response.status_code == 200

        form = csv_upload()
        form.file = locations
        assert form.validate

test_email = "deletion@tobedeleted.com"
test_password = "passwordasda123"

@pytest.mark.parametrize(
    ("message","email", "password"),(( b"Invalid username or password","w242fwa@432353.com", "somevalue"),
     (b"Invalid username or password","235423525@325235e.com", "235235")),
)
def test_bad_password_in_login(client, email, password, message):
    response = client.post("/login", data={"email": "email", "password": "password"}, follow_redirects=True)
    assert response.status_code == 200

def test_invalid_login(client, application):

    somestatuscode = client.post("/login", data={"email": "testsfdsdf2@example.com", "password": "aasfsdfsdfasf"}, follow_redirects=True)
    assert somestatuscode.status_code == 200

@pytest.mark.parametrize(
    ("email", "message", "password"),
    (("someemail@asdas.com", b"Invalid username or password", "test",),
     ("asdasdasd@anotheroen1.com", b"Invalid username or password", "aasdasddas")),
)
def test_bad_username_emaillogin(client, email, password, message):
    response = client.post("/login", data=dict(email=email, password=password), follow_redirects=True)

    assert message in response.data

def test_adding_location(application):
    with application.app_context():
        assert db.session.query(Location).count() == 0
        location = Location('title', 52, 53, 250)

        db.session.add(location)
        db.session.commit()

        location = Location.query.filter_by(title='title').first()

        assert location.title == 'title'

def test_adding_multiplelocations(application):
    with application.app_context():
        assert db.session.query(Location).count() == 0

        location1 = Location('title', 138, 163, 142240)
        db.session.add(location1)
        db.session.commit()
        location2 = Location('title', 234, 1235, 213124)
        db.session.add(location2)
        db.session.commit()

        locationa = Location.query.filter_by(title='title').first()
        locationb = Location.query.filter_by(title='title').first()
        assert locationa.title == 'title'
        assert locationb.title == 'title'

def test_dashboard__logged_users(client):
    client.post("/login",
                data={"email": "someqweqeemail@j.com",
                      "password": "123151351421", "confirm": "1212323456"})


    response = client.post("/dashboard", follow_redirects=True)

    code = 405
    assert response.status_code == code

def test_successful_login(client):
    client.post("/register", data=dict(email=test_email, password=test_password, confirm=test_password),
                follow_redirects=True)
    response = client.post("/login", data={"email": test_email, "password": test_password}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_successful_registration(client, application):
    response = client.post("/register",
                           data={"email": "user_to_be_delete@delete.org", "password": "test1234",
                                 "confirm": "test1234"},
                           follow_redirects=True)
    assert b"Congratulations, you are now a registered user!" in response.data

def test_dashboard_allow(client):
    response = client.get("/dashboard")
    code = 302
    assert code == response.status_code == 302

def test_deny_dashboard_access(client):
    response = client.post("/dashboard", follow_redirects=True)
    code = 405
    assert code == response.status_code == 405

def test_delete_location(client, application):
    application.test_client_class = FlaskLoginClient
    user1 = User('admin1@admin.com', 'Admin123', 1)
    user2 = User('admin22@admin.com', 'Admin1234', 1)

    location = Location("title", "longitude", "latitude", "population")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(location)
    db.session.commit()

    assert db.session.query(User).count() == 2
    assert db.session.query(Location).count() == 1

    with application.test_client(user=user1) as client:
        response = client.post('/locations/1/delete', follow_redirects=True)
        assert b'Location was Deleted' in response.data

