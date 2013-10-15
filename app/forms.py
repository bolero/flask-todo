__author__ = 'Bolero'

#from flask_wtf import Form, IntegerField, TextField, DateField, Required, SelectField
from flask_wtf import Form
from wtforms import IntegerField, TextField, DateField, SelectField, PasswordField
from wtforms.validators import InputRequired, Required, Email, EqualTo, Length


class AddTask(Form):
    #task_id = IntegerField('Task Id')
    name = TextField('Task Name', validators=[InputRequired()])
    due_date = DateField('Due Date (mm/dd/yy)', validators=[InputRequired()], format='%m/%d/%Y')
    priority = SelectField('Priority', validators=[InputRequired()], choices=[('1', '1'),
                                                                         ('2', '2'),
                                                                         ('3', '3'),
                                                                         ('4', '4'),
                                                                         ('5', '5')])
    status = IntegerField('Status')
    posted_date = DateField('Posted Date (mm/dd/yy)', validators=[InputRequired()], format='%m/%d/%Y')


class RegisterForm(Form):
    name = TextField('Username', validators=[InputRequired(), Length(min=6, max=25)])
    email = TextField('Email', validators=[InputRequired(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password',
                                                                                     message='Passwords must match')])


class LoginForm(Form):
    name = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])