from flask import escape, request, render_template, url_for, flash, redirect, abort
from flask_login import login_user, current_user, logout_user, login_required
from strain_library.models import *
from strain_library import app, db, bcrypt
from strain_library.forms import *
from sqlalchemy import desc
import pandas as pd
from werkzeug.utils import secure_filename
import os


@app.route('/')
@app.route('/home')
@login_required
def home():
    strains = Strain.query.all()
    return render_template('home.html', strains=strains)

@app.route('/search_strain', methods=['GET', 'POST'])
@login_required
def search_strain():
    form = SearchStrainForm()
    form.host.choices = [(h.name, h.name) for h in Host.query.order_by('name')]
    if form.validate_on_submit():
        query_host = Strain.host.contains(form.host.data)
        query_number = Strain.number.contains(form.number.data)
        query_name = Strain.name.contains(form.name.data)
        query_vector = Strain.vector.contains(form.vector.data)
        query_vector_type = Strain.vector_type.contains(form.vector_type.data)
        query_selection_marker = Strain.selection_marker.contains(form.selection_marker.data)
        query_box = Strain.box.contains(form.box.data)
        query_slot = Strain.slot.contains(form.slot.data)
        strains = Strain.query.filter(query_number, query_name, query_host, query_vector, query_vector_type, query_selection_marker, query_box, query_slot).all()
        return render_template('results.html', strains=strains)
    return render_template('search_strain.html', form=form, legend='Search strain')

@app.route('/results')
@login_required
def results():
    host = request.args.get('host')
    box = request.args.get('box')
    if host:
        strains = Strain.query.filter_by(host=host).all()
        return render_template('results.html', strains=strains)
    if box:
        strains = Strain.query.filter_by(box=box).all()
        return render_template('results.html', strains=strains)
    strains = Strain.query.all()
    return render_template('results.html', strains=strains)

@app.route('/select_host', methods=['GET', 'POST'])
@login_required
def select_host():
    hosts = Host.query.all()
    form = SelectHostForm()
    form.host.choices = [(h.name, h.name) for h in Host.query.order_by('name')]
    value = dict(form.host.choices).get(form.host.data)
    if form.validate_on_submit():
        return redirect(url_for('new_strain', host_id = value))
    return render_template('select_host.html', form=form)

@app.route('/new_strain/', methods=['GET', 'POST'])
@login_required
def new_strain():
    host_id = request.args.get('host_id')
    hosts = Host.query.all()
    boxes = Box.query.all()
    selection_markers = SelectionMarker.query.all()
    form = NewStrainForm()
    form.host.choices = [host_id]
    form.box.choices = [(b.name, b.name) for b in Box.query.order_by('name')]
    form.selection_marker.choices = [(s.name, s.name) for s in SelectionMarker.query.order_by('name')]
    if host_id == hosts[0].name:
        if form.validate_on_submit():
            new_strain = EcoliStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = EcoliStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    elif host_id == hosts[1].name:
        if form.validate_on_submit():
            new_strain = HvolcaniiStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = HvolcaniiStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    elif host_id == hosts[2].name:
        if form.validate_on_submit():
            new_strain = SpombeStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = SpombeStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    elif host_id == hosts[3].name:
        if form.validate_on_submit():
            new_strain = ScerevisiaeStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = ScerevisiaeStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    elif host_id == hosts[4].name:
        if form.validate_on_submit():
            new_strain = YenterocoliticaStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = YenterocoliticaStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    elif host_id == hosts[5].name:
        if form.validate_on_submit():
            new_strain = VparahaemolyticusStrain(number=form.number.data, name=form.name.data, host=host_id, vector=form.vector.data, vector_type=form.vector_type.data, selection_marker=form.selection_marker.data, box=form.box.data, slot=form.slot.data, date_of_creation=form.date_of_creation.data, comments=form.comments.data, author=current_user)
            db.session.add(new_strain)
            db.session.commit()
            flash('Submitted succesfully!', 'success')
            return render_template('new_strain.html', form=form, hosts=hosts, boxes=boxes, selection_markers=selection_markers, legend='New strain')
        elif request.method == 'GET':
            strain = VparahaemolyticusStrain.query.order_by(desc(Strain.id))
            try:
                form.number.data = strain[0].number[:2] + str(int(strain[0].number[2:]) + 1)
            except IndexError:
                form.number.data = (host_id.split()[0][0] + host_id.split()[1][0] + str(1)).upper()
    else:
        flash('This host is not in the database. Please ask the admin to take care of it!', 'danger')
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

@app.route("/strain/<int:strain_id>/")
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
    form.host.choices = [(h.name, h.name) for h in Host.query.order_by('name')]
    form.box.choices = [(b.name, b.name) for b in Box.query.order_by('name')]
    form.selection_marker.choices = [(s.name, s.name) for s in SelectionMarker.query.order_by('name')]
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

@app.route("/upload_many_select_host", methods=['GET', 'POST'])
@login_required
def upload_many_select_host():
    hosts = Host.query.all()
    form = SelectHostForm()
    form.host.choices = [(h.name, h.name) for h in Host.query.order_by('name')]
    value = dict(form.host.choices).get(form.host.data)
    if form.validate_on_submit():
        return redirect(url_for('upload_many', host_id=value))
    return render_template('select_host.html', form=form)


@app.route("/upload_many", methods=['GET', 'POST'])
@login_required
def upload_many():
    host_id = request.args.get('host_id')
    form = UploadMany()
    form.host.choices = [host_id]
    hosts = Host.query.all()
    if host_id == hosts[0].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass

                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = EcoliStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = EcoliStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    elif host_id == hosts[1].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass

                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = HvolcaniiStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = HvolcaniiStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    elif host_id == hosts[2].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass

                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = SpombeStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = SpombeStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    elif host_id == hosts[3].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass

                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = ScerevisiaeStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = ScerevisiaeStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    elif host_id == hosts[4].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass

                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = YenterocoliticaStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = YenterocoliticaStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    elif host_id == hosts[5].name:   
        if form.validate_on_submit():
            if form.file:
                strain_list = pd.read_excel(form.file.data)
                df_boxes = strain_list['Box'].to_list()
                for df_b in df_boxes:
                    box = Box.query.filter_by(name=df_b).first()
                    if not box:
                        new_box = Box(name=df_b)
                        db.session.add(new_box)
                    else:
                        pass

                df_selection_markers = strain_list['Selection marker'].to_list()
                for df_sm in df_selection_markers:
                    sm = SelectionMarker.query.filter_by(name=df_sm).first()
                    if not sm:
                        new_selection_marker = SelectionMarker(name=df_sm)
                        db.session.add(new_selection_marker)
                    else:
                        pass
                    
                db.session.commit()
                for _, row in strain_list.iterrows():
                    try:
                        single_strain = VparahaemolyticusStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=row['Date of creation'].date(), comments=row['Comments'], author=current_user)
                    except AttributeError:
                        single_strain = VparahaemolyticusStrain(number=row['Number'], name=row['Name'], host=host_id, vector=row['Vector'], vector_type=row['Vector type'], selection_marker=row['Selection marker'], box=row['Box'], slot=row['Slot'], date_of_creation=None, comments=row['Comments'], author=current_user)
                    db.session.add(single_strain)
            db.session.commit()
            flash('The library has been uploaded!', 'success')
            return redirect(url_for('home'))
    
   
    return render_template('upload_many.html', form=form)