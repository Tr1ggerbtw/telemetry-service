from app.conftest import client

def register_and_login(client):
    client.post('/register', json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    response = client.post('/login', json={
        "email": "test@gmail.com",
        "password": "123456"
    })
    return response.json['token']

def test_create_location_success(client):
    token = register_and_login(client)
    response = client.post('/locations', json={ "name": "home"}, 
                headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201

def test_create_location_invalid_name(client):
    token = register_and_login(client)
    response = client.post('/locations', json={ "name": ""}, 
                headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
    
