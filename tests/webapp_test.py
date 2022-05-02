import pytest

from web_app import create_app

@pytest.fixture(scope="module")
def test_client():
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()

def test_home(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert b"Home" in response.data

def test_about(test_client):
    response = test_client.get("/about")
    assert response.status_code == 200
    assert b"<h1>Application Overview</h1>" in response.data

def test_recipes(test_client):
    response = test_client.get("/recipes")
    assert response.status_code == 200
    assert b"Recipe Generator" in response.data

# def test_groceries(test_client):
#     response = test_client.get("/groceries")
#     assert response.status_code == 200
#     assert b"Personal Grocery List" in response.data

# def test_list(test_client):
#     response = test_client.get("/list")
#     assert response.status_code == 200
#     assert b"Custom Recipe List" in response.data

def test_help(test_client):
    response = test_client.get("/help")
    assert response.status_code == 200
    assert b"List of All Possible Inputs For Recipe Generator" in response.data

def test_login(test_client):
    response = test_client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data




