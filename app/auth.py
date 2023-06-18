import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=("GET", "POST"))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (usernam, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(
                    url_for("auth.login")
                )
            flash(error)
    return render_template('auth/register.html')


@bp.route('/login', method=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
    
    
        ).fetchone()

        if user is None:
            error = "Incorrect Username."

        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    """This function checks if a user's id is stored in that session, 
    no matter what URL is requested"""

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

    
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(
        url_for('index')
    )


def login_required(view):
    """Creating, editing, and deleting blog posts will require a user to be
      logged in. A decorator can be used to check this for each view it's applied to"""
    
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
