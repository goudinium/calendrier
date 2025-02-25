from flask import url_for

def test_app_is_under_testing_mode(app):
    assert app.testing 

def test_user_is_redirected_to_login_page_if_not_connected(client):
    response = client.get("/", follow_redirects=True)
    assert response.request.path == "/login"

def test_login(client, auth):
    assert client.get("/login").status_code == 200
    response = auth.login()
    assert response.request.path == "/calendar"
    assert b"Bonjour" in response.data

def test_user_cannot_access_future_calendar_days(client, auth):
    auth.login()
    with client:
        response = client.get("/day/15", follow_redirects=True)
        assert response.request.path == "/calendar"

def test_user_cannot_access_days_after_24th_december(client, auth):
    auth.login()
    with client:
        assert client.get("/day/25", follow_redirects=True).status_code == 404

def test_answer_is_submitted_correctly(client, auth):
    auth.login()
    with client:
        answer = {"answer_character": "Agathe",
                  "answer_time": "something",
                  "answer_place": "something",
                  "answer_sound": "something",
                  "answer_object": "something",
                  "answer_color": "something",
                  "submit": "Valider"}
        response = client.post("/day/10", data = answer, follow_redirects=True)
        assert "Ta réponse enregistrée" in response.data.decode()

def test_user_cannot_see_answer(client, auth):
    auth.login()
    with client:
        answer = {"answer_character": "Agathe",
                  "answer_time": "something",
                  "answer_place": "something",
                  "answer_sound": "something",
                  "answer_object": "something",
                  "answer_color": "something",
                  "submit": "Valider"}
        response = client.post("/day/10", data = answer, follow_redirects=True)
        assert "Ta réponse enregistrée" in response.data.decode()
        assert "answer-10" not in response.data.decode()

def test_user_who_did_not_answer_can_see_answer(client, auth): 
    auth.login()
    with client:
        response = client.get("/day/9", follow_redirects=True)
        assert "Ta réponse enregistrée" not in response.data.decode()
        assert "answer-9" in response.data.decode()