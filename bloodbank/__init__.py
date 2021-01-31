import os

from flask_mail import Message, Mail
from flask import Flask

# application factory function
def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'bloodbank.sqlite'),
    )
    app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'testingbloodbank@gmail.com',
    MAIL_PASSWORD = 'ALal1029',
))
    mail = Mail()
    mail.init_app(app)
     # load the instance config, if it exists, when not testing
  

    app.secret_key = 'development key'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import bank
    app.register_blueprint(bank.bp)
    app.add_url_rule('/', endpoint='index')

    return app