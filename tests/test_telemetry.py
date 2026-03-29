from app.conftest import client

def create_sensor(client):
    client.post('/register', json={"email": "test@gmail.com", "password": "123456"})
    response = client.post('/login', json={"email": "test@gmail.com", "password": "123456"})
    token = response.json['token']
    
    client.post('/locations', json={"name": "home"},
                headers={"Authorization": f"Bearer {token}"})
    
    client.post('/create-sensor', json={
        "mac_address": "AA:BB:CC:DD:EE:FF",
        "location_id": 1
    }, headers={"Authorization": f"Bearer {token}"})

def test_send_telemetry_success(client):
    create_sensor(client)
    response = client.post('/telemetry-send', json={
        "sensor_id": 1,
        "value": 50
    })
    assert response.status_code == 201

def test_send_telemetry_invalid_value(client):
    response = client.post('/telemetry-send', json={
        "sensor_id": 1,
        "value": 999
    })
    assert response.status_code == 400

def test_send_telemetry_sensor_not_found(client):
    response = client.post('/telemetry-send', json={
        "sensor_id": 999,
        "value": 50
    })
    assert response.status_code == 404

