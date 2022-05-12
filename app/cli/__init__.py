import os

import click
from flask.cli import with_appcontext

from app import config
from app.db import db, database


@click.command(name='create-db')
@with_appcontext
def create_database():
    # get root directory of project
    root = os.path.dirname(os.path.abspath(__file__))
    # set the name of the apps log folder to logs
    dbdir = os.path.join(root, '../../database')
    # make a directory if it doesn't exist
    if not os.path.exists(dbdir):
        os.mkdir(dbdir)
    db.create_all()

@click.command(name='create-log-folder')
@with_appcontext
def create_log_folder():
    # get root directory of project
    root = os.path.dirname(os.path.abspath(file))
    # set the name of the apps log folder to logs
    log_dir = os.path.join(root, '../../logs')
    # make a directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
