def test_create_blacklist(client):
    payload = {"plate_text": "mp 09 ab 1234 ", "reason": "unregistered"}
    response = client.post("/api/alerts/blacklist", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["plate_text"] == "MP09AB1234"
    assert data["reason"] == "unregistered"
    assert data["flagged_at"].endswith("Z")

def test_blacklist_upsert(client):
    payload1 = {"plate_text": "MP09AB1234", "reason": "unregistered"}
    response1 = client.post("/api/alerts/blacklist", json=payload1)
    assert response1.status_code == 201
    assert response1.json()["reason"] == "unregistered"

    payload2 = {"plate_text": "mp09ab1234", "reason": "fine_due"}
    response2 = client.post("/api/alerts/blacklist", json=payload2)
    assert response2.status_code == 201
    assert response2.json()["reason"] == "fine_due"
