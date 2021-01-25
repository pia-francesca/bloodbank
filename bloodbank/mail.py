from flask_mail import Mail, Message
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bloodbank.db import get_db

bp = Blueprint('mail', __name__)



mail = Mail(app)

@bp.route("/contact", methods=('GET', 'POST'))
def contact():
    if request.method == 'POST':
        message= request.form['Message']
        sender= request.form ['Sender']
        recipients = request.form ['Recipient']
        body= request.form['body']

        Message(message, sender = sender, recipients = recipients)
        msg.body = body
        mail.send(message)
   return "Sent"