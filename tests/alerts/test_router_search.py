from datetime import datetime, timezone
from app.main import app
from app.alerts.router import get_trajectory_provider
from app.alerts.schemas import TrajectoryResult, TrajectorySighting
from tests.conftest import FakeTrajectoryProvider

def test_search_not_blacklisted(client):
    response = client.get("/api/alerts/search/mp09ab1234")
    assert response.status_code == 200
    data = response.json()
    assert data["plate"] == "MP09AB1234"
    assert data["blacklisted"] is False
    assert data["reason"] is None
    assert data["flagged_at"] is None
    assert "trajectory" in data
    assert data["trajectory"] == {"found": False, "sightings": []}

def test_search_blacklisted_with_trajectory(client):
    # Blacklist plate first
    client.post("/api/alerts/blacklist", json={"plate_text": "mp09ab1234 ", "reason": "fine_due"})

    # Setup fake trajectory response
    canned_sighting = TrajectorySighting(
        camera_id="CAM_01",
        location_name="MG Road Junction",
        gps_lat=23.1815,
        gps_lng=79.9864,
        timestamp=datetime(2026, 8, 26, 10, 32, 15, tzinfo=timezone.utc),
        direction_from_prev=None,
        speed_from_prev_kmh=None
    )
    fake_provider = FakeTrajectoryProvider(
        canned_result=TrajectoryResult(found=True, sightings=[canned_sighting])
    )
    app.dependency_overrides[get_trajectory_provider] = lambda: fake_provider

    response = client.get("/api/alerts/search/MP09AB1234")
    assert response.status_code == 200
    data = response.json()
    assert data["plate"] == "MP09AB1234"
    assert data["blacklisted"] is True
    assert data["reason"] == "fine_due"
    assert data["flagged_at"].endswith("Z")
    assert data["trajectory"]["found"] is True
    assert len(data["trajectory"]["sightings"]) == 1
    assert data["trajectory"]["sightings"][0]["camera_id"] == "CAM_01"
    assert data["trajectory"]["sightings"][0]["timestamp"] == "2026-08-26T10:32:15Z"
