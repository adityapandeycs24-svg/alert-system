from datetime import datetime, timezone
from app.alerts.models import Alert

def test_acknowledge_success(client, session):
    alert = Alert(
        plate_text="MP09AB1234",
        camera_id="CAM_01",
        location_name="Loc 1",
        timestamp=datetime(2026, 8, 26, 10, 0, 0, tzinfo=timezone.utc),
        reason="fine_due",
        acknowledged=False
    )
    session.add(alert)
    session.commit()

    response = client.post(f"/api/alerts/feed/{alert.id}/acknowledge")
    assert response.status_code == 200
    assert response.json() == {"id": alert.id, "acknowledged": True}

def test_acknowledge_not_found(client):
    response = client.post("/api/alerts/feed/9999/acknowledge")
    assert response.status_code == 404
    assert response.json() == {
        "error": True,
        "message": "Alert not found",
        "status_code": 404
    }
