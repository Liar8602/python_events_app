from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from app.user.models import User
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Send', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={'class': 'form-control'})
    first_name = StringField('Name', validators=[DataRequired()], render_kw={'class': 'form-control'})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={'class': 'form-control'})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'class': 'form-control'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'class': 'form-control'})
    password2 = PasswordField('Retry password', validators=[DataRequired(), EqualTo('password')],
                              render_kw={'class': 'form-control'})
    profile_picture = FileField('Photo', validators=[FileAllowed(['jpg', 'png'])])
    birthday = DateField('Birthday', format='%d.%n.%Y')
    gender = RadioField('Sex', choices=[('male', 'Male'), ('female', 'Female')])
    submit = SubmitField('Send', render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError('User with this name was registered')

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError('User with this email was been registered')
