from datetime import datetime, timezone
from app.alerts.interfaces import SightingEvent, process_sighting, StubTrajectoryProvider
from app.alerts.service import AlertService

def test_process_sighting_creates_alert(session):
    # First add plate to blacklist
    service = AlertService(db=session, trajectory_provider=StubTrajectoryProvider())
    service.add_to_blacklist("MP09AB1234", "fine_due")

    sighting = SightingEvent(
        plate_text="mp 09 ab 1234",
        camera_id="CAM_02",
        location_name="Wright Town Circle",
        timestamp=datetime(2026, 8, 26, 10, 37, 40, tzinfo=timezone.utc)
    )

    alert = process_sighting(db=session, sighting=sighting)
    assert alert is not None
    assert alert.plate_text == "MP09AB1234"
    assert alert.camera_id == "CAM_02"
    assert alert.location_name == "Wright Town Circle"
    assert alert.reason == "fine_due"
    assert alert.acknowledged is False

def test_process_sighting_ignores_non_blacklisted(session):
    sighting = SightingEvent(
        plate_text="MP09XYZ999",
        camera_id="CAM_02",
        location_name="Wright Town Circle",
        timestamp=datetime(2026, 8, 26, 10, 37, 40, tzinfo=timezone.utc)
    )
    alert = process_sighting(db=session, sighting=sighting)
    assert alert is None
