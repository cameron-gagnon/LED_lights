from wtforms import StringField, BooleanField, Form
from wtforms.validators import DataRequired

class LoginForm(Form):

    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)
