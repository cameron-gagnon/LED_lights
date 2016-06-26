from super_secret import USERNAME, PASSWORD
import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'asdf1234asdf1234'

MAIL = {
    'MAIL_SERVER':   'localhost',
    'MAIL_PORT':     25,
    'MAIL_USERNAME': USERNAME,
    'MAIL_PASSWORD': PASSWORD,
    'ADMINS': ['cameron.gagnon@gmail.com'],
}
