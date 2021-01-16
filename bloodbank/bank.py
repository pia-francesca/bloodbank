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
        'SELECT bs.id, type, blood_type, rhesus, created, bs.bloodbank_id, username'
        ' FROM bloodstock bs JOIN user u ON bs.bloodbank_id = u.bloodbank_id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('bank/index.html', bloodstock=bloodstock)

