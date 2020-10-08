from datetime import datetime
from strain_library import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    Strain = db.relationship('Strain', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Strain(db.Model):
    __tablename__ = 'strain'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    host = db.Column(db.String, nullable=False)
    vector = db.Column(db.String)
    vector_type = db.Column(db.String)
    selection_marker = db.Column(db.String)
    box = db.Column(db.String)
    slot = db.Column(db.String)
    date_of_creation = db.Column(db.Date)
    comments = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String)

    __mapper_args__ = {
        'polymorphic_identity':'strain',
        'polymorphic_on':type
    }

    def __repr__(self):
        return f"Strain('{self.number}', '{self.name}')"

class EcoliStrain(Strain):
    __tablename__ = 'ecolistrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'ecolistrainlist'
    }

class HvolcaniiStrain(Strain):
    __tablename__ = 'hvolcaniistrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'hvolcaniistrainlist'
    }

class SpombeStrain(Strain):
    __tablename__ = 'spombestrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'spombestrainlist'
    }

class ScerevisiaeStrain(Strain):
    __tablename__ = 'scerevisiaestrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'scerevisiaestrainlist'
    }

class VparahaemolyticusStrain(Strain):
    __tablename__ = 'vparahaemolyticusstrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'vparahaemolyticusstrainlist'
    }

class YenterocoliticaStrain(Strain):
    __tablename__ = 'yenterocoliticastrainlist'
    id = db.Column(db.Integer, db.ForeignKey('strain.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'yenterocoliticastrainlist'
    }

class Box(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class Host(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

class SelectionMarker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)