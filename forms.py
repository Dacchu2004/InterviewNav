from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileAllowed

# Form for CV upload
class CVUploadForm(FlaskForm):
    cv_file = FileField('Upload CV', validators=[
        DataRequired(),
        FileAllowed(['pdf', 'doc', 'docx'], 'PDF and Word documents only!')
    ])
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=50)])
    job_role = StringField('Job Role', validators=[DataRequired(), Length(max=50)])
    interview_level = SelectField('Interview Level', 
                                  choices=[('Beginner', 'Beginner'), 
                                           ('Intermediate', 'Intermediate'), 
                                           ('Advanced', 'Advanced')], 
                                  validators=[DataRequired()])
    submit = SubmitField('Submit')

# Form for user registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

