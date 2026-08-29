from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
from sqlalchemy.orm import Session

from app.alerts.schemas import TrajectoryResult
from app.alerts.models import Alert
from app.alerts.repository import BlacklistRepository, AlertRepository

@dataclass
class SightingEvent:
    plate_text: str
    camera_id: str
    location_name: str
    timestamp: datetime

def process_sighting(
    db: Session,
    sighting: SightingEvent,
    blacklist_repo: BlacklistRepository | None = None,
    alert_repo: AlertRepository | None = None
) -> Alert | None:
    """
    Internal function called per sighting from ANPR module ingestion pipeline.
    Normalizes plate, checks Blacklist, creates Alert if matched, else returns None.
    """
    # Normalize plate text
    normalized_plate = sighting.plate_text.upper().replace(" ", "")

    if blacklist_repo is None:
        blacklist_repo = BlacklistRepository(db)
    if alert_repo is None:
        alert_repo = AlertRepository(db)

    blacklist_entry = blacklist_repo.get_by_plate(normalized_plate)
    if not blacklist_entry:
        return None

    alert = alert_repo.create(
        plate_text=normalized_plate,
        camera_id=sighting.camera_id,
        location_name=sighting.location_name,
        timestamp=sighting.timestamp,
        reason=blacklist_entry.reason,
        acknowledged=False
    )
    return alert

class TrajectoryProvider(Protocol):
    def get_trajectory(self, plate: str) -> TrajectoryResult:
        ...

class StubTrajectoryProvider:
    def get_trajectory(self, plate: str) -> TrajectoryResult:
        return TrajectoryResult(found=False, sightings=[])
