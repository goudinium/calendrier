def test_user_is_redirected_to_login_page_if_not_connected(client):
    response = client.get("/", follow_redirects=True)
    assert response.request.path == "/login"

