from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegistrationForm(FlaskForm):
    name = StringField(render_kw={'placeholder': 'Name'}, validators=[DataRequired()])
    email = StringField(render_kw={'placeholder': 'Email'}, validators=[DataRequired()])
    password = StringField(render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    submit = SubmitField(render_kw={'placeholder': 'Register'})


# TODO: Create a LoginForm to login existing users
class LoginForm(FlaskForm):
    email = StringField(render_kw={'placeholder': 'Email'}, validators=[DataRequired()])
    password = StringField(render_kw={'placeholder': 'Password'}, validators=[DataRequired()])
    submit = SubmitField(render_kw={'placeholder': 'Login'})


# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    body = CKEditorField('Comment', render_kw={'placeholder': 'Enter your comment here'})
    submit = SubmitField('Submit')



