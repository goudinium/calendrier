from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = '74f98e76805cca74c37072e4f2e715af'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

moch_day = 23

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from petitcalendrier import routes