from flask_wtf import FlaskForm
from wtforms.validators import  DataRequired, Email, EqualTo
from wtforms import ValidationError, StringField, SubmitField, TextAreaField, PasswordField
from flask_wtf.file import FileField, FileAllowed
# from myproject import db

dr = DataRequired()
class LoginForm(FlaskForm):

    email = StringField("Email", validators=[dr])
    password = StringField("Password", validators=[dr])
    submit = SubmitField("Login")

class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[dr])
    email = StringField("Email", validators=[dr])
    password = StringField("Password", validators=[dr, EqualTo('pass_confirm', message='Password Must Match')])
    pass_confirm = StringField("Confirm Password", validators=[dr])
    submit = SubmitField("Register")

class UpdateUserForm(FlaskForm):

    picture = FileField('Update Profile Picture', validators=[dr, FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Update Profile") 

class BlogPostsForm(FlaskForm):

    text = TextAreaField(render_kw={"placeholder":'Whats on your mind?', 'rows':3, 'cols':60})
    picture = FileField('Add Photo', validators=[dr, FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField("Post")
    