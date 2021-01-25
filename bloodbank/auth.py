import functools
import re

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from bloodbank.db import get_db


# creates blueprint named 'auth':
bp = Blueprint('auth', __name__, url_prefix='/auth')


def password_check(password):

    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # calculating the length
    length_error = len(password) < 8

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )
    
    return {
        'password is ok' : password_ok,
        'password should be 8 characters' : length_error,
        'password should contain a number' : digit_error,
        'Password should contain an uppercase letter' : uppercase_error,
        'Password should contain an uppercase letter' : lowercase_error,
        'Password should contain a symbol' : symbol_error,
    }


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        bloodbank_id = request.form['bloodbank_id']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not password_check(password)['password is ok']:
            if password_check(password).keys:
                error= password_check(password)
    
        elif not bloodbank_id:
            error = 'Connection to a bloodbank is required.'
        elif db.execute(
            'SELECT id FROM bloodbank WHERE id = ?', (bloodbank_id,)
        ).fetchone() is None:
            error = 'There is no bloodbank registered with this ID.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'There is already an account registered with this name {}.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, bloodbank_id) VALUES (?, ?, ?)',
                (username, generate_password_hash(password), bloodbank_id)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
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
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('bank.overview'))

        flash(error)

    return render_template('auth/login.html')


# register a function that runs before the view function, no matter what URL is requested
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# logout
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# for access to data base check if a user is loaded and redirects to the login page otherwise
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
