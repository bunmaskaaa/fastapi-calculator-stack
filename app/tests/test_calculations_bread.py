# app/tests/test_calculations_bread.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.main import app
from app.database import get_db
from app import models
from .utils import override_get_db, create_test_user_and_token  # adjust names to your helpers

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def auth_headers(token: str):
    return {"Authorization": f"Bearer {token}"}

def test_add_and_browse_calculations():
    db: Session
    user, token = create_test_user_and_token()

    payload = {
        "operation": "add",
        "operand1": 10,
        "operand2": 5,
    }
    resp = client.post("/calculations/", json=payload, headers=auth_headers(token))
    assert resp.status_code == 201
    data = resp.json()
    assert data["result"] == 15.0

    resp2 = client.get("/calculations/", headers=auth_headers(token))
    assert resp2.status_code == 200
    calculations = resp2.json()
    assert len(calculations) >= 1
    assert any(c["id"] == data["id"] for c in calculations)

def test_read_edit_delete_calculation():
    user, token = create_test_user_and_token()

    payload = {"operation": "multiply", "operand1": 2, "operand2": 3}
    resp = client.post("/calculations/", json=payload, headers=auth_headers(token))
    assert resp.status_code == 201
    calc = resp.json()
    calc_id = calc["id"]

    # Read
    r = client.get(f"/calculations/{calc_id}", headers=auth_headers(token))
    assert r.status_code == 200
    assert r.json()["result"] == 6.0

    # Edit
    update_payload = {"operand2": 4}
    r2 = client.patch(f"/calculations/{calc_id}", json=update_payload, headers=auth_headers(token))
    assert r2.status_code == 200
    assert r2.json()["result"] == 8.0  # 2 * 4

    # Delete
    r3 = client.delete(f"/calculations/{calc_id}", headers=auth_headers(token))
    assert r3.status_code == 204

    # Ensure gone
    r4 = client.get(f"/calculations/{calc_id}", headers=auth_headers(token))
    assert r4.status_code == 404

def test_cannot_see_others_calculations():
    user1, token1 = create_test_user_and_token(email="user1@example.com")
    user2, token2 = create_test_user_and_token(email="user2@example.com")

    payload = {"operation": "add", "operand1": 1, "operand2": 1}
    resp = client.post("/calculations/", json=payload, headers=auth_headers(token1))
    calc_id = resp.json()["id"]

    # user2 tries to read
    r = client.get(f"/calculations/{calc_id}", headers=auth_headers(token2))
    assert r.status_code == 404