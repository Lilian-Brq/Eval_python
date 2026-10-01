import pytest

STATION = {"code": "ST01", "name": "Gare", "ville": "Rouen", "capacity": 10, "status": "open"}

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_create_then_read(client):
    r = client.post("/stations", json=STATION)
    assert r.status_code == 201
    station_id = r.json()["id"]

    r2 = client.get(f"/stations/{station_id}")
    assert r2.status_code == 200
    assert r2.json()["code"] == STATION["code"]
    assert r2.json()["name"] == STATION["name"]

def test_filter_status_open(client):
    client.post("/stations", json=STATION)
    client.post("/stations", json={**STATION, "code": "ST02", "status": "closed"})
    r = client.get("/stations?status=open")
    assert r.status_code == 200
    assert all(s["status"] == "open" for s in r.json())

def test_patch_name(client):
    client.post("/stations", json=STATION)
    r = client.patch("/stations/1", json={"name": "Nouveau Nom"})
    assert r.status_code == 200
    assert r.json()["name"] == "Nouveau Nom"
    assert r.json()["code"] == STATION["code"]
    assert r.json()["capacity"] == STATION["capacity"]
    assert r.json()["status"] == STATION["status"]

def test_get_not_found(client):
    r = client.get("/stations/999")
    assert r.status_code == 404
    assert r.json()

@pytest.mark.parametrize("payload", [
    {**STATION, "capacity": 0},
    {**STATION, "status": "flying"},
])
def test_invalid_entries(client, payload):
    r = client.post("/stations", json=payload)
    assert r.status_code == 422
    assert client.get("/stations").json() == []

def test_duplicate_code(client):
    client.post("/stations", json=STATION)
    r = client.post("/stations", json=STATION)
    assert r.status_code == 409
    assert len(client.get("/stations").json()) == 1