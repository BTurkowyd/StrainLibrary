from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from strain_library.models import *


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That user name is taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already in use.')


class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember')
    submit = SubmitField('Sign In')


class NewStrainForm(FlaskForm):
    number = StringField('Number', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    host = SelectField('Host', validators=[DataRequired()])
    vector = StringField('Vector', validators=[Optional()])
    vector_type = StringField('Vector type', validators=[Optional()])
    selection_marker = SelectMultipleField('Selection marker', validators=[Optional()])
    box = SelectMultipleField('Box', validators=[DataRequired()])
    slot = StringField('Slot', validators=[DataRequired()])
    date_of_creation = DateField(
        'Date of submission', format='%m/%d/%Y', validators=[Optional()])
    comments = TextAreaField('Comments', validators=[Optional()])
    submit = SubmitField('Submit')

    # def validate_number(self, number):
    #     strain = Strain.query.filter_by(number=number.data).first()
    #     if strain:
    #         raise ValidationError('This strain number is already in use.')


class NewBoxForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        box = Box.query.filter_by(name=name.data).first()
        if box:
            raise ValidationError('This box already exists.')


class NewHostForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        host = Host.query.filter_by(name=name.data).first()
        if host:
            raise ValidationError('This host already exists.')


class NewSelectionMarkerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        selection_marker = SelectionMarker.query.filter_by(
            name=name.data).first()
        if selection_marker:
            raise ValidationError('This selection marker already exists.')


class SelectHostForm(FlaskForm):
    host = SelectField('Host', validators=[DataRequired()])
    submit = SubmitField('Next')


class UploadMany(FlaskForm):
    file = FileField('Table', validators=[FileRequired()])
    submit = SubmitField('Upload')