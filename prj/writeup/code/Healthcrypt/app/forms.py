# IMPORT STATEMENTS

from flask_wtf           import FlaskForm

from wtforms             import StringField, PasswordField

from wtforms             import TextAreaField, SubmitField

from wtforms.validators  import ValidationError, Length

from wtforms.validators  import DataRequired, EqualTo

from app.models          import Physician

from cryptography.fernet import Fernet

# WEB FORM CLASSES

# LOGIN FORM
class LoginForm(FlaskForm):

  username = StringField("Username",   validators=[DataRequired()])

  password = PasswordField("Password", validators=[DataRequired()])

  submit   = SubmitField("Sign In")

# REGISTRATION FORM
class RegistrationForm(FlaskForm):

  username = StringField("Username",   validators=[DataRequired()])

  fname    = StringField("First Name", validators=[DataRequired()])

  lname    = StringField("Last Name",  validators=[DataRequired()])

  userpwd  = PasswordField("Password", validators=[DataRequired()])

  userpwd2 = PasswordField("Repeat Password",
    validators=[DataRequired(), EqualTo("userpwd")])

  submit = SubmitField("Register")

  def validate_username(self, username):

    user = Physician.query.filter_by(username=username.data).first()

    if user is not None:

      raise ValidationError("Please use a different username.")

# RECORD FORM
class RecordForm(FlaskForm):

  patfname = StringField("Patient First Name",    validators=[DataRequired()])

  patlname = StringField("Patient Last Name",     validators=[DataRequired()])
  
  patdob   = StringField("Patient Date of Birth", validators=[DataRequired()])

  patdiag  = TextAreaField("Patient Diagnosis",
    validators=[DataRequired(), Length(min=1, max=250)])

  submit = SubmitField("Submit")
