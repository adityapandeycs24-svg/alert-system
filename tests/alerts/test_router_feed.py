from datetime import datetime, timezone
from app.alerts.models import Alert

def test_feed_ordering_and_filtering(client, session):
    # Insert test alerts with different timestamps
    alert1 = Alert(
        plate_text="MP09AB1234",
        camera_id="CAM_01",
        location_name="Loc 1",
        timestamp=datetime(2026, 8, 26, 10, 0, 0, tzinfo=timezone.utc),
        reason="fine_due",
        acknowledged=False
    )
    alert2 = Alert(
        plate_text="MP09CD5678",
        camera_id="CAM_02",
        location_name="Loc 2",
        timestamp=datetime(2026, 8, 26, 10, 10, 0, tzinfo=timezone.utc),
        reason="stolen",
        acknowledged=True
    )
    alert3 = Alert(
        plate_text="MP09EF9012",
        camera_id="CAM_03",
        location_name="Loc 3",
        timestamp=datetime(2026, 8, 26, 10, 20, 0, tzinfo=timezone.utc),
        reason="unregistered",
        acknowledged=False
    )
    session.add_all([alert1, alert2, alert3])
    session.commit()

    # Test GET /feed default (most recent first)
    response = client.get("/api/alerts/feed")
    assert response.status_code == 200
    feed = response.json()
    assert len(feed) == 3
    assert feed[0]["id"] == alert3.id
    assert feed[1]["id"] == alert2.id
    assert feed[2]["id"] == alert1.id
    assert feed[0]["timestamp"] == "2026-08-26T10:20:00Z"

    # Test unacknowledged_only filter
    response_unack = client.get("/api/alerts/feed?unacknowledged_only=true")
    assert response_unack.status_code == 200
    feed_unack = response_unack.json()
    assert len(feed_unack) == 2
    assert feed_unack[0]["id"] == alert3.id
    assert feed_unack[1]["id"] == alert1.id
