from flask_wtf import FlaskForm
from wtforms.fields import SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp

class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired(), Email("Enter email")])
    password=PasswordField("Password", validators=[InputRequired('Enter password')])
    submit = SubmitField("Login")

class ResetPasswordForm(FlaskForm):
    new_password=PasswordField("New Password", validators=[InputRequired('Enter password'), Length(min=12), Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
                message="Password must include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )])
    confirm_password=PasswordField("Confirm New Password", validators=[InputRequired('Enter password'), Length(min=12), EqualTo('new_password', message='Passwords must match.'), Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
                message="Password must include at least one uppercase letter, one lowercase letter, one number, and one special character."
            )])
    submit = SubmitField("Reset")
    
    
    
    