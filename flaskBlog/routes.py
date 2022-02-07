from flask import render_template, url_for, flash, redirect, request
from importlib_metadata import email
from flaskBlog import app, db, bcrypt
from flaskBlog.forms import RegistrationForm, LoginForm, UpdateAccount
from flaskBlog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author':'me',
        'title': 'Bird',
        'content' : 'yom beans',
        'date': 'wow/a/date'
    },
    {
        'author':'u',
        'title': 'Wow Blog',
        'content' : 'yems bird',
        'date': 'wow/a/date'
    } 
    ]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Already logged in dum dum', 'danger')
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'You, {form.username.data}, have successfully followed instructions', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Already logged in dum dum', 'danger')
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Questionable choice but welcome back!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('You seem to have forgotten something..unlucky', 'danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccount()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Wowow Details changed!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = "Example"
        form.email.data = "example@gmail.com"
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title = 'Profile', image_file = image_file, form=form)