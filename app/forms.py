from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, StringField

from wtforms import validators, ValidationError


class EmailForm(FlaskForm):
    recipient = StringField("To", [validators.InputRequired('Recipient is required'), validators.Email('Input should be a email address')])
    subject = StringField("Subject", [validators.InputRequired('Subject is required')])
    message = TextAreaField("Message", [validators.InputRequired('Message is required')])