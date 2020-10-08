from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf import CsrfProtect

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app = Flask(__name__)

app.config['SECRET_KEY'] = 'db8ea46832fd645d9cfce8c1c002bb1d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///strain_library.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
crsf = CsrfProtect()

crsf.init_app(app)

from strain_library import routes