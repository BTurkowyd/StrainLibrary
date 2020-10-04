from flask import escape, request, render_template, url_for, flash, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from strain_library.models import *
from strain_library import app, db, bcrypt
from strain_library.forms import *
from sqlalchemy import desc


@app.route('/')
@app.route('/home')
@login_required
def home():
    strains = Strain.query.all()
    return render_template('home.html', strains=strains)

@app.route('/search_strain')
@login_required
def search_strain():
    return render_template('search_strain.html')

@app.route('/new_strain', methods=['GET', 'POST'])
@login_required
def new_strain():
    hosts = Host.query.all()
    boxes = Box.query.all()
    selection_markers = SelectionMarker.query.all()
    strain = Strain.query.order_by(desc(Strain.id))
    form = NewStrainForm()
    form.host.choices = [(h.id, h.name) for h in Host.query.order_by('name')]
    form.box.choices = [(b.id, b.name) for b in Box.query.order_by('name')]
    form.selection_marker.choices = [(s.id, s.name) for s in SelectionMarker.query.order_by('name')]
    if form.validate_on_submit():
        new_strain = Strain(number=form.number.data, name=form.name.data, host=form.host.data, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
        db.session.add(new_strain)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
    elif request.method == 'GET':
        try:
            form.number.data = strain[0].number[:-1] + str(int(strain[0].number[-1]) + 1)
        except IndexError:
            form.number.data = None
    return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')

@app.route('/new_box', methods=['GET', 'POST'])
@login_required
def new_box():
    form = NewBoxForm()
    if form.validate_on_submit():
        new_box = Box(name=form.name.data)
        db.session.add(new_box)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return render_template('new_box.html', form=form)
    return render_template('new_box.html', form=form)

@app.route('/new_host', methods=['GET', 'POST'])
@login_required
def new_host():
    form = NewHostForm()
    if form.validate_on_submit():
        new_host = Host(name=form.name.data)
        db.session.add(new_host)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return render_template('new_host.html', form=form)
    return render_template('new_host.html', form=form)

@app.route('/new_selection_marker', methods=['GET', 'POST'])
@login_required
def new_selection_marker():
    form = NewSelectionMarkerForm()
    if form.validate_on_submit():
        new_selection_marker = SelectionMarker(name=form.name.data)
        db.session.add(new_selection_marker)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return render_template('new_selection_marker.html', form=form)
    return render_template('new_selection_marker.html', form=form)

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

@app.route("/strain/<int:strain_id>")
@login_required
def strain(strain_id):
    strain = Strain.query.get_or_404(strain_id)
    return render_template('strain.html', title=strain.name, strain=strain)

@app.route("/strain/<int:strain_id>/update", methods=['GET', 'POST'])
@login_required
def update_strain(strain_id):
    strain = Strain.query.get_or_404(strain_id)
    hosts = Host.query.all()
    boxes = Box.query.all()
    form = NewStrainForm()
    form.host.choices = [(h.id, h.name) for h in Host.query.order_by('name')]
    form.box.choices = [(b.id, b.name) for b in Box.query.order_by('name')]
    form.selection_marker.choices = [(s.id, s.name) for s in SelectionMarker.query.order_by('name')]
    if form.validate_on_submit():
        strain.number = form.number.data
        strain.name = form.name.data
        strain.vector = form.vector.data
        strain.vector_type = form.vector_type.data
        strain.selection_marker = form.selection_marker.data
        strain.box = form.box.data
        strain.slot = form.slot.data
        strain.date_of_creation = form.date_of_creation.data
        strain.comments = form.comments.data
        db.session.commit()
        flash('The strain has been updated!', 'success')
        return redirect(url_for('strain', strain_id=strain.id))
    elif request.method == 'GET':
        form.number.data = strain.number
        form.name.data = strain.name
        form.vector.data = strain.vector
        form.vector_type.data = strain.vector_type
        form.selection_marker.data = strain.selection_marker
        form.box.data = strain.box
        form.slot.data = strain.slot
        form.date_of_creation.data = strain.date_of_creation
        form.comments.data = strain.comments
    return render_template('new_strain.html', form=form, legend='Update Strain')

@app.route("/strain/<int:strain_id>/delete", methods=['POST'])
@login_required
def delete_strain(strain_id):
    strain = Strain.query.get_or_404(strain_id)
    db.session.delete(strain)
    db.session.commit()
    flash('Your strain has been deleted!', 'success')
    return redirect(url_for('home'))