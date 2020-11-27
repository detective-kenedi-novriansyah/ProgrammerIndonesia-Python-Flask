from flask_wtf import FlaskForm
from wtforms import FileField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    profile = FileField("Profile", validators=[DataRequired()])
    submit = SubmitField("Update Profile")

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class UserRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self,username):
        user =  User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username sudah ada, silahkan cari yang lain")

    def validate_email(self,email):
        user =  User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email sudah ada, silahkan cari yang lain")
