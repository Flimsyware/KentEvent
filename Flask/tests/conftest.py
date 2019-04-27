import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import DBHelper

@pytest.fixture
def app():
    db_fd, db_path = ':memory:'

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        DBHelper()

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()