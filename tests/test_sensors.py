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

def test_create_sensor_success(client):
    token = register_and_login(client)
    
    client.post('/locations', json={"name": "home"}, 
                headers={"Authorization": f"Bearer {token}"})
    
    response = client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201

def test_create_sensor_unauthorized(client):
    response = client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    })
    assert response.status_code == 401

def test_create_sensor_forbidden(client):
    token = register_and_login(client)
    response = client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 884145
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403

def test_create_sensor_duplicate_mac(client):
    token = register_and_login(client)
    
    client.post('/locations', json={"name": "home"},
                headers={"Authorization": f"Bearer {token}"})
    
    client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    response = client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 409

# delete scenarios

def test_delete_sensor_success(client):
    token = register_and_login(client)
    
    client.post('/locations', json={"name": "home"},
                headers={"Authorization": f"Bearer {token}"})
    
    client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})

    response = client.delete('/delete-sensor', json={"sensor_id": 1},
                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204

def test_delete_sensor_forbidden(client):
    token = register_and_login(client)
    
    client.post('/locations', json={"name": "home"},
                headers={"Authorization": f"Bearer {token}"})
    
    client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})

    client.post('/register', json={
        "email": "hacker@gmail.com",
        "password": "123456"
    })
    first_response = client.post('/login', json={
        "email": "hacker@gmail.com",
        "password": "123456"
    })

    hacker_token = first_response.json['token']

    response = client.delete('/delete-sensor', json={"sensor_id": 1},
                             headers={"Authorization": f"Bearer {hacker_token}"})
    assert response.status_code == 403

    