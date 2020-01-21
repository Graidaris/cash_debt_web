from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import (StringField, PasswordField, DateField, 
                     FloatField, BooleanField, SubmitField)

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()] )
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
    
    
class RegisterForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired()] )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Registration")