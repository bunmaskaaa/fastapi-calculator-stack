# app/tests/test_users_integration.py

def test_register_and_login_flow(client):
    # Register new user
    register_payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "Secret123",
    }

    res = client.post("/users/register", json=register_payload)
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == register_payload["email"]
    assert "id" in data

    # Register with same email should fail
    res_dup = client.post("/users/register", json=register_payload)
    assert res_dup.status_code == 400

    # Login with correct credentials
    login_payload = {
        "email": "alice@example.com",
        "password": "Secret123",
    }
    res_login = client.post("/users/login", json=login_payload)
    assert res_login.status_code == 200
    login_data = res_login.json()
    assert login_data["user"]["email"] == "alice@example.com"
    assert login_data["message"] == "Login successful"

    # Login with wrong password should fail
    bad_login = {
        "email": "alice@example.com",
        "password": "WrongPass",
    }
    res_bad = client.post("/users/login", json=bad_login)
    assert res_bad.status_code == 401