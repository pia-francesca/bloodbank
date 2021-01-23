from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

from bloodbank.auth import login_required
from bloodbank.db import get_db

bp = Blueprint('bank', __name__)


@bp.route('/')
def index():
    return render_template('bank/index.html')


@bp.route('/overview')
@login_required
def overview():
    user_id = session.get('user_id')
    db = get_db()
    bloodstock = db.execute(
        ' SELECT bs.id, blood_type, blood_group, rhesus, created, room, fridge, shelf, bs.bloodbank_id, username'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' ORDER BY created DESC',(user_id,)
    ).fetchall()

    return render_template('bank/overview.html', bloodstock=bloodstock)


@bp.route('/input', methods=('GET', 'POST'))
@login_required
def input():
    if request.method == 'POST':
        id = request.form['id']
        blood_type = request.form['blood_type']
        blood_group = request.form['blood_group']
        rhesus = request.form['rhesus']
        room = request.form['room']
        fridge = request.form['fridge']
        shelf = request.form['shelf']
        created = request.form['created']

        error = None

        if not id:
            error = 'ID is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO bloodstock (id, blood_type, blood_group, rhesus, room, fridge, shelf, created, bloodbank_id)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (id, blood_type, blood_group, rhesus, room, fridge, shelf, created, g.user['bloodbank_id'])
            )
            db.commit()
            return redirect(url_for('bank.overview'))

    return render_template('bank/input.html')


@bp.route('/remove', methods = ('GET', 'POST'))
@login_required
def remove():
    if request.method == 'POST':
        user_id = session.get('user_id')
        blood_id = request.form['blood_id']
        db = get_db()
        
        error = None

        if db.execute(
            'SELECT bs.id'
            ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
            ' WHERE bs.id = ?', (user_id, blood_id, )
        ).fetchone() is None:
            error = 'The blood bag with the ID {} is not in your bloodbank.'.format(blood_id)
        
        if error is not None:
            flash(error)
        else:
            db.execute('DELETE FROM bloodstock WHERE id = ?', (blood_id,))
            db.commit()

    return render_template('bank/remove.html')


@bp.route("/settings")
@login_required
def settings():
    user_id = session.get('user_id')
    db = get_db()
    bloodbank = db.execute(
        'SELECT b.id, name FROM bloodbank b, user u WHERE u.id = ? AND u.bloodbank_id = b.id', (user_id,)
    ).fetchall()
    
    return render_template('bank/settings.html', bloodbank = bloodbank)