from app.conftest import client

def test_register_success(client):
    response = client.post('/register', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })
    assert response.status_code == 201

def test_register_duplicate_email(client):
    client.post('/register', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })

    response = client.post('/register', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })
    assert response.status_code == 409

def test_register_missing_password(client):
    response = client.post('/register', json={
        "email": "greatemail@gmail.com"
    })
    assert response.status_code == 400

def test_login_success(client):
    client.post('/register', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })
    response = client.post('/login', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })
    assert response.status_code == 200
    assert "token" in response.json

def test_login_wrong_password(client):
    client.post('/register', json={
        "email": "greatemail@gmail.com",
        "password": "11111111"
    })
    response = client.post('/login', json={
        "email": "greatemail@gmail.com",
        "password": "not11111111"
    })
    assert response.status_code == 401

def test_login_user_not_found(client):
    response = client.post('/login', json={
        "email": "whoisbro@gmail.com",
        "password": "????????"
    })
    assert response.status_code == 401