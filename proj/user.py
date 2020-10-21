from flask_wtf import FlaskForm
import email_validator
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class Registration(FlaskForm):
	fname = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	lname = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	phone = StringField('Phone Number', validators=[DataRequired()])

	email = StringField('Email', validators=[DataRequired(), Email()])

	passwd = PasswordField('Password', validators=[DataRequired()])

	conPass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('passwd')])

	submit = SubmitField('Register')


class Login(FlaskForm):
	usrname = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])

	emaill = StringField('Email', validators=[DataRequired(), Email()])

	passwdd = PasswordField('Password', validators=[DataRequired()])

	remember = BooleanField('Remember Me')

	submitt = SubmitField('Login')
