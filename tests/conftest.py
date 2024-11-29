import pytest 
from petitcalendrier import create_app, db, bcrypt
from petitcalendrier.models import User, Question

class TestConfig():
    SECRET_KEY = '74f98e76805cca74c37072e4f2e715af'
    SQLALCHEMY_DATABASE_URI = 'sqlite://' 
    TESTING = True
    WTF_CSRF_ENABLED = False
    DAY = 10

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='admin', password='fanfan'):
        return self._client.post(
            '/login',
            data={'username': username, 'password': password, 'remember':'y', 'submit': 'Connexion'},
            follow_redirects=True
        )

    def logout(self):
        return self._client.get('/logout')

@pytest.fixture()
def app():
    app = create_app(TestConfig)
    
    with app.app_context():
        db.create_all()
        # creating one admin in the db
        pwd = bcrypt.generate_password_hash("fanfan").decode('utf-8')
        admin = User(username='admin', first_name="François", last_name="Goudineau", password=pwd, is_admin=True)
        db.session.add(admin)
        db.session.commit()

        # creating fake questions
        for day in range(1, 25):
            q = Question(day=day, image=f"img-{day}", answer=f"answer-{day}", solution_time="", solution_object="", solution_place="", solution_sound="", solution_color="")
            db.session.add(q)
        db.session.commit()
        
    yield app 

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture
def auth(client):
    return AuthActions(client)
