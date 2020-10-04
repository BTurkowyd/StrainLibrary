from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from strain_library.models import User, Strain

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
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
    vector = StringField('Vector', validators=[Optional()])
    vector_type = StringField('Vector type', validators=[Optional()])
    selection_marker = StringField('Selection marker', validators=[Optional()])
    box = StringField('Box', validators=[DataRequired()])
    slot = StringField('Slot', validators=[DataRequired()])
    date_of_creation = DateField('Date of submission', format='%m/%d/%Y', validators=[Optional()])
    comments = TextAreaField('Comments', validators=[Optional()])
    submit = SubmitField('Submit')

    def validate_number(self, number):
        strain = Strain.query.filter_by(number=number.data).first()
        if strain:
            raise ValidationError('This strain number is already in use.')