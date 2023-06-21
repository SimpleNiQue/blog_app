import os
import tempfile

import pytest
from app import create_app
from app.models import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as fp:
    _data_sql = fp.read().decode('utf-8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            'TESTING': True,
            'DATABASE': db_path
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

