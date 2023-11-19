from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField   
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField("Login: ", validators=[DataRequired(), Length(min=4, max=50)])
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=50)])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Sign in")