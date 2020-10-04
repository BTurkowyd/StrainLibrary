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
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    vector = db.Column(db.String)
    vector_type = db.Column(db.String)
    selection_marker = db.Column(db.String)
    box = db.Column(db.String)
    slot = db.Column(db.String)
    date_of_creation = db.Column(db.Date)
    comments = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Strain('{self.number}', '{self.name}')"