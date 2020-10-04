from flask import escape, request, render_template, url_for, flash, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from strain_library.models import User, Strain
from strain_library import app, db, bcrypt
from strain_library.forms import RegistrationForm, LoginForm, NewStrainForm


@app.route('/')
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/search_strain')
@login_required
def search_strain():
    return render_template('search_strain.html')

@app.route('/new_strain', methods=['GET', 'POST'])
@login_required
def new_strain():
    form = NewStrainForm()
    if form.validate_on_submit():
        new_strain = Strain(number=form.number.data, name=form.name.data, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
        db.session.add(new_strain)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return render_template('new_strain.html', form=form)
    return render_template('new_strain.html', form=form)

@app.route('/new_box')
@login_required
def new_box():
    return render_template('new_box.html')

@app.route('/new_host')
@login_required
def new_host():
    return render_template('new_host.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for {form.username.data} created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
