import os
from config import basedir, MAIL
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

if not app.debug:
    import logging

    # mail logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL['MAIL_USERNAME'] or MAIL['MAIL_PASSWORD']:
        credentials = (MAIL['MAIL_USERNAME'], MAIL['MAIL_PASSWORD'])
    mail_handler = SMTPHandler((MAIL['MAIL_SERVER'], MAIL['MAIL_PORT']),
            'no-reply@' + MAIL['MAIL_SERVER'], MAIL['ADMINS'],
            'Pixelator failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    # log file
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/pixel.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('pixel startup')


# putting this import after the `app = Flask(__name__)` line prevents
# circular imports
from app import views, models
