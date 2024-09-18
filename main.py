import os
from datetime import date
from flask import Flask, abort, render_template, redirect, url_for, flash, current_app, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.exc import IntegrityError
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CommentForm, LoginForm, RegistrationForm
from forms import CreatePostForm
from smtplib import SMTP, SMTPException

'''
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('API_KEY')
MY_EMAIL = os.environ.get('MyEMAIL')
RECIPIENT = os.environ.get('RECIPIENT')
PASSWORD = os.environ.get('PASSWORD')
ckeditor = CKEditor(app)
Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///posts.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Initialize Gravatar
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    use_ssl=True,
                    base_url=None)
app.jinja_env.globals['gravatar'] = gravatar


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    # Relationship to User - Each post is associated with one author
    author = db.relationship('User', back_populates='posts')


# TODO: Create a User table for all your registered users. 
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    # Relationship to BlogPost - One user can have many blog posts
    posts = db.relationship('BlogPost', back_populates='author', lazy=True)
    # Relationship to Comment - One user can have many comments
    comments = db.relationship('Comment', back_populates='user', lazy=True)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    # Relationship to User - Each comment is associated with one user
    user = db.relationship('User', back_populates='comments')


with app.app_context():
    db.create_all()

from functools import wraps
from flask import redirect, url_for, flash


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You must be an admin to access this page.', 'danger')
            return redirect(url_for('get_all_posts'))
        return f(*args, **kwargs)

    return decorated_function


# TODO: Use Werkzeug to hash the user's password when creating a new user.
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data, salt_length=8)

        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please log in instead.", "warning")
            return redirect(url_for('login'))

        # Create a new user and add to the database
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # flash("Registration successful! You can now log in.", "success")
        login_user(new_user)
        return redirect(url_for('get_all_posts'))

    return render_template("register.html", form=form)


# TODO: Retrieve a user from the database based on their email.
@app.route('/login', methods=['GET', 'POST'])
def login():
    year = date.today().year
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Invalid Email, Please Sign Up...', 'danger')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Incorrect Password, please try again', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        # flash('Login Successful!', 'success')
        return redirect(url_for('get_all_posts'))
    return render_template("login.html", form=form, current_year=year)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    year = date.today().year

    # Check if there are any users in the database
    first_user = User.query.first()

    # If no users exist, redirect to the register page
    if not first_user:
        flash("No users found. Please register first.", "info")
        return redirect(url_for('register'))
    else:
        # Fetch the first user and set them as admin
        first_user.is_admin = True
        db.session.commit()
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts, current_year=year)


# TODO: Allow logged-in users to comment on posts
@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    year = date.today().year
    requested_post = db.get_or_404(BlogPost, post_id)
    is_admin = current_user.id == 1
    comments = Comment.query.filter_by(post_id=post_id).all()
    form = CommentForm()

    if form.validate_on_submit():
        new_comment = Comment(
            text=form.body.data,
            user_id=current_user.id,
            post_id=post_id,
            email=current_user.email
        )
        db.session.add(new_comment)
        db.session.commit()
        # flash('Comment added successfully!', 'success')
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post, comments=comments, form=form, current_year=year)


# TODO: Use a decorator so only an admin user can create a new post
@app.route("/new-post", methods=["GET", "POST"])
@login_required
@admin_required
def add_new_post():
    year = date.today().year
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author_id=current_user.id,
            date=date.today().strftime("%B %d, %Y")
        )
        try:
            db.session.add(new_post)
            db.session.commit()
        except IntegrityError:
            flash('A post with that title already exists.', 'danger')
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, current_year=year)


# TODO: Use a decorator so only an admin user can edit a post
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=current_user.name,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, admin=current_user.is_admin)


# TODO: Use a decorator so only an admin user can delete a post
@app.route("/delete/<int:post_id>")
@login_required
@admin_required
def delete_post(post_id):
    if not current_user.is_admin:
        abort(403)
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    year = date.today().year
    return render_template("about.html", current_year=year)


@app.route("/contact", methods=['GET', 'POST'])
@login_required
def contact():
    year = date.today().year
    if request.method == 'POST':
        sender = request.form.get('name')
        sender_email = request.form.get('email')
        phone_number = request.form.get('phone')
        message = request.form.get('message')
        subject = 'You Have New Message From Yomex-B'
        try:
            with SMTP('smtp.gmail.com', 587) as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=PASSWORD)
                connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECIPIENT,
                                    msg=f'Subject:{subject}\n\nSender: {sender}\nPhone: {phone_number}\n'
                                        f'Email: {sender_email}\nMessage: {message}')
            flash('Thanking you for the Feedback!!!')
            return redirect(url_for('get_all_posts'))
        except SMTPException as e:
            flash(f"Failed to send email. Please try again later. Error: {str(e)}")
            return redirect(url_for('contact'))

    return render_template("contact.html", current_year=year)


if __name__ == "__main__":
    app.run(debug=False)
