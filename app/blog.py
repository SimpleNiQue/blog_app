from flask import (
    url_for, render_template, Blueprint,
    flash, g, redirect, request
    )
from werkzeug.exceptions import abort

from app.auth import login_required
from app.models import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post  p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)
