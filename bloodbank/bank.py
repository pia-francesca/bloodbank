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


@bp.route('/overview_old')
@login_required
def overview_old():
    user_id = session.get('user_id')
    db = get_db()
    bloodstock = db.execute(
        ' SELECT bs.id, blood_type, blood_group, rhesus, created, room, fridge, shelf, bs.bloodbank_id, username'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' ORDER BY created DESC',(user_id,)
    ).fetchall()

    return render_template('bank/overview_old.html', bloodstock=bloodstock)


@bp.route('/overview')
@login_required
def overview():
    user_id = session.get('user_id')
    db = get_db()

    erythrocytes = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes"',(user_id,)
    ).fetchone()

    plasma = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma"',(user_id,)
    ).fetchone()

    thrombocytes = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes"',(user_id,)
    ).fetchone()

    erythrocytes_A_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "A" AND rhesus = "+"',(user_id,)
    ).fetchone()

    erythrocytes_A_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "A" AND rhesus = "-"',(user_id,)
    ).fetchone()

    erythrocytes_B_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "B" AND rhesus = "+"',(user_id,)
    ).fetchone()

    erythrocytes_B_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "B" AND rhesus = "-"',(user_id,)
    ).fetchone()
    
    erythrocytes_AB_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "AB" AND rhesus = "+"',(user_id,)
    ).fetchone()
    
    erythrocytes_AB_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "AB" AND rhesus = "-"',(user_id,)
    ).fetchone()

    erythrocytes_O_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "O" AND rhesus = "+"',(user_id,)
    ).fetchone()

    erythrocytes_O_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "erythrocytes" AND blood_group = "O" AND rhesus = "-"',(user_id,)
    ).fetchone()

    plasma_A_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "A" AND rhesus = "+"',(user_id,)
    ).fetchone()

    plasma_A_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "A" AND rhesus = "-"',(user_id,)
    ).fetchone()

    plasma_B_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "B" AND rhesus = "+"',(user_id,)
    ).fetchone()

    plasma_B_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "B" AND rhesus = "-"',(user_id,)
    ).fetchone()

    plasma_AB_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "AB" AND rhesus = "+"',(user_id,)
    ).fetchone()

    plasma_AB_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "AB" AND rhesus = "-"',(user_id,)
    ).fetchone()

    plasma_O_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "O" AND rhesus = "+"',(user_id,)
    ).fetchone()

    plasma_O_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "plasma" AND blood_group = "O" AND rhesus = "-"',(user_id,)
    ).fetchone()

    thrombocytes_A_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "A" AND rhesus = "+"',(user_id,)
    ).fetchone()

    thrombocytes_A_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "A" AND rhesus = "-"',(user_id,)
    ).fetchone()

    thrombocytes_B_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "B" AND rhesus = "+"',(user_id,)
    ).fetchone()
 
    thrombocytes_B_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "B" AND rhesus = "-"',(user_id,)
    ).fetchone()

    thrombocytes_AB_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "AB" AND rhesus = "+"',(user_id,)
    ).fetchone()

    thrombocytes_AB_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "AB" AND rhesus = "-"',(user_id,)
    ).fetchone()

    thrombocytes_O_pos = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "O" AND rhesus = "+"',(user_id,)
    ).fetchone()

    thrombocytes_O_neg = db.execute(
        ' SELECT COUNT(*)'
        ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        ' WHERE blood_type = "thrombocytes" AND blood_group = "O" AND rhesus = "-"',(user_id,)
    ).fetchone()

    return render_template('bank/overview.html', 
                            erythrocytes = erythrocytes, 
                            plasma = plasma,
                            thrombocytes = thrombocytes,
                            erythrocytes_A_pos = erythrocytes_A_pos,
                            erythrocytes_A_neg = erythrocytes_A_neg, 
                            erythrocytes_B_pos = erythrocytes_B_pos,
                            erythrocytes_B_neg = erythrocytes_B_neg,
                            erythrocytes_AB_pos = erythrocytes_AB_pos,
                            erythrocytes_AB_neg = erythrocytes_AB_neg,
                            erythrocytes_O_pos = erythrocytes_O_pos,
                            erythrocytes_O_neg = erythrocytes_O_neg,
                            plasma_A_pos = plasma_A_pos,
                            plasma_A_neg = plasma_A_neg,
                            plasma_B_pos = plasma_B_pos,
                            plasma_B_neg = plasma_B_neg,
                            plasma_AB_pos = plasma_AB_pos,
                            plasma_AB_neg = plasma_AB_neg,
                            plasma_O_pos = plasma_O_pos,
                            plasma_O_neg = plasma_O_neg,
                            thrombocytes_A_pos = thrombocytes_A_pos,
                            thrombocytes_A_neg = thrombocytes_A_neg,
                            thrombocytes_B_pos = thrombocytes_B_pos,
                            thrombocytes_B_neg = thrombocytes_B_neg,
                            thrombocytes_AB_pos = thrombocytes_AB_pos,
                            thrombocytes_AB_neg = thrombocytes_AB_neg,
                            thrombocytes_O_pos = thrombocytes_O_pos,
                            thrombocytes_O_neg = thrombocytes_O_neg)


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


@bp.route('/search', methods = ('GET', 'POST'))
@login_required
def search():
    if request.method == 'POST':
        user_id = session.get('user_id')
        blood_type = request.form['blood_type']
        blood_group = request.form['blood_group']
        rhesus = request.form['rhesus']
        
        db = get_db()
        
        error = None

        #if db.execute(
        #    'SELECT bs.id'
        #    ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
        #    ' WHERE bs.id = ?', (user_id, blood_id, )
        #).fetchone() is None:
        #    error = 'The blood bag with the ID {} is not in your bloodbank.'.format(blood_id)

        if db.execute(
            ' SELECT bs.id'
            ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
            ' WHERE blood_type = ? AND blood_group = ? AND rhesus = ?'
            ' ORDER BY created ASC, room, fridge, shelf',(user_id, blood_type, blood_group, rhesus)
        ).fetchone() is None:
            flash('None found.')
        elif error is not None:
            flash(error)
        else:
            blood_search = db.execute(
            ' SELECT bs.id, created, room, fridge, shelf, blood_type, blood_group, rhesus'
            ' FROM bloodstock bs JOIN (SELECT * FROM user WHERE id = ?) u ON bs.bloodbank_id = u.bloodbank_id'
            ' WHERE blood_type = ? AND blood_group = ? AND rhesus = ?'
            ' ORDER BY created ASC, room, fridge, shelf',(user_id, blood_type, blood_group, rhesus)
            ).fetchall()
            return render_template('bank/search.html', blood_search = blood_search)
    return render_template('bank/search.html')