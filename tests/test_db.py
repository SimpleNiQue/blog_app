import sqlite3

import pytest
from app.models import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as err:
        db.execute('SELECT 1')

    assert 'closed' in str(err.value)