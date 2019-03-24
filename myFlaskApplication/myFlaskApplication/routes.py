import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from myFlaskApplication import myFlaskApp, db, bcrypt, mail
from myFlaskApplication.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                      PostForm, RequestResetForm, ResetPasswordForm)
from myFlaskApplication.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@myFlaskApp.route("/")
@myFlaskApp.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template('home.html', posts=posts, title='Home Page!')


@myFlaskApp.route("/about")
def about():
    return render_template('about.html', title='About Page!')


@myFlaskApp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf=8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!, please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@myFlaskApp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Welcome! {user.email}', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login failed!', 'danger')
    return render_template('login.html', title='Login', form=form)


@myFlaskApp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    file_name = random_hex + file_ext
    picture_path = os.path.join(myFlaskApp.root_path, 'static/profile_pics', file_name)

    i = Image.open(form_picture)
    i.thumbnail((125, 125))
    i.save(picture_path)

    return file_name


@myFlaskApp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            if current_user.image_file != "default.jpg":
                image_file_curr = os.path.join(myFlaskApp.root_path, 'static/profile_pics', current_user.image_file)
                os.remove(image_file_curr)
            current_user.image_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@myFlaskApp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Posted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form)


@myFlaskApp.route('/post/<int:post_id>', methods=['GET'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title="post.title", post=post)


@myFlaskApp.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Post Updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('update_post.html', title="post.title", post=post, form=form)


@myFlaskApp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post was deleted!', 'success')
    return redirect(url_for('home'))


@myFlaskApp.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.\
        filter_by(author=user).\
        order_by(Post.date_posted.desc()).\
        paginate(page=page, per_page=4)
    return render_template('user_posts.html', posts=posts, user=user, title=user.username + "'s Page!")


def send_reset_email(user):
    token = user.get_reset_token()
    message = Message('Password Reset Request',
                      sender='noreply@blog.com',
                      recipients=[user.email])
    message.body = f'''Hello Blogger!

Please follow the link to reset password:
{url_for('reset_password', token=token, _external=True)}

Warm Regards,
Flask Blog Team
'''
    mail.send(message)


@myFlaskApp.route("/forgot_password", methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # send_reset_email(user)
        token = user.get_reset_token()
        flash('An email has been sent to your registered email to reset the password!', 'info')
        return redirect(url_for('reset_password', token=token, _external=True))
    return render_template('forgot_password.html', form=form)


@myFlaskApp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token has expired or invalid!', 'warning')
        return redirect(url_for('forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf=8')
        user.password = hashed_password
        db.session.commit()
        flash('Password reset was successful!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
