# app/tests/test_calculations_integration.py
import pytest


def route_exists(client, path: str, method: str) -> bool:
    """
    Helper to check if a given path+method exists on the FastAPI app.
    """
    for route in client.app.routes:
        if getattr(route, "path", None) == path:
            methods = getattr(route, "methods", set()) or set()
            if method.upper() in methods:
                return True
    return False


def test_calculation_crud_flow(client):
    # Only run this test if our /calculations/ endpoints are actually present
    if not route_exists(client, "/calculations/", "POST"):
        pytest.skip("Calculations BREAD endpoints not available in this environment")

    # Create
    create_payload = {
        "operation": "add",
        "operand_a": 2.0,
        "operand_b": 3.0,
        "result": 5.0,
    }
    res_create = client.post("/calculations/", json=create_payload)
    assert res_create.status_code == 201
    calc = res_create.json()
    calc_id = calc["id"]
    assert calc["result"] == 5.0

    # Browse
    res_list = client.get("/calculations/")
    assert res_list.status_code == 200
    all_calcs = res_list.json()
    assert any(c["id"] == calc_id for c in all_calcs)

    # Read
    res_get = client.get(f"/calculations/{calc_id}")
    assert res_get.status_code == 200
    assert res_get.json()["id"] == calc_id

    # Edit (PUT)
    update_payload = {
        "operation": "add",
        "operand_a": 10.0,
        "operand_b": 5.0,
        "result": 15.0,
    }
    res_put = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert res_put.status_code == 200
    assert res_put.json()["result"] == 15.0

    # Partial Edit (PATCH)
    patch_payload = {"result": 20.0}
    res_patch = client.patch(f"/calculations/{calc_id}", json=patch_payload)
    assert res_patch.status_code == 200
    assert res_patch.json()["result"] == 20.0

    # Delete
    res_del = client.delete(f"/calculations/{calc_id}")
    assert res_del.status_code == 204

    # Confirm gone
    res_get_missing = client.get(f"/calculations/{calc_id}")
    assert res_get_missing.status_code == 404


def test_invalid_calculation_data_triggers_error(client):
    if not route_exists(client, "/calculations/", "POST"):
        pytest.skip("Calculations BREAD endpoints not available in this environment")

    # Missing required fields -> FastAPI/Pydantic should return 422
    bad_payload = {"operation": "add"}  # no operand_a, operand_b, result
    res = client.post("/calculations/", json=bad_payload)
    assert res.status_code == 422