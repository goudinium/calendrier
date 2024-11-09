from petitcalendrier import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(60), unique=False, nullable=False)
    last_name = db.Column(db.String(60), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.first_name} {self.last_name}', '{self.is_admin}')"
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, unique = True, nullable = False)
    answer = db.Column(db.String(60), unique=False, nullable=False)
    image = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"Question('{self.day}', '{self.answer}')"