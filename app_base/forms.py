from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import  FileAllowed



class RegistrationForm(FlaskForm):
    username = StringField('user name',validators=[DataRequired(), Length(min = 2, max = 100)])
    firstname = StringField("first name", validators=[DataRequired(), Length(min = 2, max = 100)])
    lastname = StringField("last name", validators=[DataRequired(), Length(min = 2, max = 100)])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('SignUp')

class EditForm(FlaskForm):
    username = StringField('user name',validators=[DataRequired(), Length(min = 2, max = 100)])
    firstname = StringField("first name", validators=[DataRequired(), Length(min = 2, max = 100)])
    lastname = StringField("last name", validators=[DataRequired(), Length(min = 2, max = 100)])
    submit = SubmitField('update')


class RequestPassReset(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('send verification email')

class ConfirmPassReset(FlaskForm):
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('reset password')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('login')


class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    article = TextAreaField("Article", validators=[DataRequired()])
    source = StringField("Source", validators=[DataRequired()])
    photos = MultipleFileField('Image', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Submit")

class EmailConfirm(FlaskForm):
    email = StringField("Enter your Email", validators=[DataRequired(),Email()])
    submit = SubmitField("Submit")
