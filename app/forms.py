from wtforms import BooleanField, Form

class LoginForm(Form):

    remember_me = BooleanField('remember_me', default=False)
