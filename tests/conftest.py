import pytest 
from petitcalendrier import app as calendar_app

@pytest.fixture()
def app():
    yield calendar_app 

@pytest.fixture()
def client(app):
    return app.test_client()
