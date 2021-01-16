from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from bloodbank.auth import login_required
from bloodbank.db import get_db

bp = Blueprint('bank', __name__)


@bp.route('/')
def index():
    db = get_db()
    bloodstock = db.execute(
        'SELECT bs.id, blood_type, blood_group, rhesus, created, room, fridge, shelf, bs.bloodbank_id, username'
        ' FROM bloodstock bs JOIN user u ON bs.bloodbank_id = u.bloodbank_id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('bank/index.html', bloodstock=bloodstock)


@bp.route('/overview')
@login_required
def overview():
    db = get_db()
    bloodstock = db.execute(
        'SELECT bs.id, blood_type, blood_group, rhesus, created, room, fridge, shelf, bs.bloodbank_id, username'
        ' FROM bloodstock bs JOIN user u ON bs.bloodbank_id = u.bloodbank_id'
        ' ORDER BY created DESC'
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

