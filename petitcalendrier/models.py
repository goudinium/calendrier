from petitcalendrier import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(60), unique=False, nullable=False)
    last_name = db.Column(db.String(60), unique=False, nullable=False) # todo: remove 
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    score = db.Column(db.Integer, unique=False, default=0)
    answers = db.relationship('Answer', backref='author', lazy=True)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.first_name} {self.last_name}', '{self.is_admin}')"
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, unique = True, nullable = False)
    image = db.Column(db.String(20), unique=False, nullable=False)
    answer = db.Column(db.String(20), unique=False, nullable=False)
    solution_time = db.Column(db.String(60), unique=False, nullable=False)
    solution_object = db.Column(db.String(60), unique=False, nullable=False)
    solution_place = db.Column(db.String(60), unique=False, nullable=False)
    solution_sound = db.Column(db.String(60), unique=False, nullable=False)
    solution_color = db.Column(db.String(60), unique=False, nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)

    def __repr__(self) -> str:
        return f"Question('{self.day}', '{self.answer}')"
    
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer_character = db.Column(db.String(20), unique=False, nullable=False)
    answer_time = db.Column(db.String(60), unique=False, nullable=False)
    answer_object = db.Column(db.String(60), unique=False, nullable=False)
    answer_place = db.Column(db.String(60), unique=False, nullable=False)
    answer_sound = db.Column(db.String(60), unique=False, nullable=False)
    answer_color = db.Column(db.String(60), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __repr__(self) -> str:
        return f"Answer('{self.answer_character}' for question {self.question_id} by '{self.user_id}')"