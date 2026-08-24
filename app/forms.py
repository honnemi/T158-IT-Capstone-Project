from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired(), Email("Enter email")])
    password=PasswordField("Password", validators=[InputRequired('Enter password')])
    submit = SubmitField("Login")
    
    