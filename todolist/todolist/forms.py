from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, DateTimeField
from wtforms.validators import DataRequired,Length
from wtforms.fields.html5 import EmailField
class LoginForm(FlaskForm):
    username= StringField('username',description="type username here",validators=[DataRequired(),Length(min=2,max=10)])
    password= PasswordField('password',description="type password here",validators=[DataRequired(),Length(min=5,max=20)])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username= StringField('username',description="type username here",validators=[DataRequired(),Length(min=2,max=10)])
    email= EmailField('email',description="type email here",validators=[DataRequired()])
    password= PasswordField('password',description="type password here",validators=[DataRequired(),Length(min=5,max=20)])
    confirm_password = PasswordField('confirm_password', description="re-enter your password here",
                             validators=[DataRequired(), Length(min=5, max=20)])
    submit = SubmitField('Register')


class TodoForm(FlaskForm):
    what_to_do = StringField('what_to_do', validators=[DataRequired()])
    due_date = DateTimeField('due_date', validators=[DataRequired()])
    status = StringField('status')
    submit = SubmitField('Add new item')