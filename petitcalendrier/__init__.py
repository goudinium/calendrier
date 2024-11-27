from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from datetime import date
from petitcalendrier.config import Config

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

db = SQLAlchemy()
bcrypt = Bcrypt()

def get_todays_day():
    return current_app.config["DAY"] if "DAY" in current_app.config else date.today().day 

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from petitcalendrier.calendar.routes import calendar
    from petitcalendrier.users.routes import users
    from petitcalendrier.main.routes import main

    app.register_blueprint(calendar)
    app.register_blueprint(users)
    app.register_blueprint(main)

    return app