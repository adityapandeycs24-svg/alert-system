from sqlalchemy.orm import Session
from app.alerts.models import Blacklist, Alert
from app.alerts.repository import BlacklistRepository, AlertRepository
from app.alerts.schemas import (
    AlertSearchResponse,
    AlertFeedItem,
    AcknowledgeResponse,
    BlacklistCreateResponse,
)
from app.alerts.interfaces import TrajectoryProvider
from app.core.errors import AppError

class AlertService:
    def __init__(self, db: Session, trajectory_provider: TrajectoryProvider):
        self.db = db
        self.blacklist_repo = BlacklistRepository(db)
        self.alert_repo = AlertRepository(db)
        self.trajectory_provider = trajectory_provider

    def normalize_plate(self, plate: str) -> str:
        """Normalizes plate text: uppercase and strip spaces."""
        return plate.upper().replace(" ", "")

    def search_plate(self, plate: str) -> AlertSearchResponse:
        norm_plate = self.normalize_plate(plate)
        blacklist_entry = self.blacklist_repo.get_by_plate(norm_plate)

        # Call trajectory_provider unconditionally
        trajectory = self.trajectory_provider.get_trajectory(norm_plate)

        if blacklist_entry:
            return AlertSearchResponse(
                plate=norm_plate,
                blacklisted=True,
                reason=blacklist_entry.reason,
                flagged_at=blacklist_entry.flagged_at,
                trajectory=trajectory
            )
        else:
            return AlertSearchResponse(
                plate=norm_plate,
                blacklisted=False,
                reason=None,
                flagged_at=None,
                trajectory=trajectory
            )

    def get_feed(self, limit: int = 20, unacknowledged_only: bool = False) -> list[AlertFeedItem]:
        alerts = self.alert_repo.list(limit=limit, unacknowledged_only=unacknowledged_only)
        return [
            AlertFeedItem(
                id=alert.id,
                plate_text=alert.plate_text,
                camera_id=alert.camera_id,
                location_name=alert.location_name,
                timestamp=alert.timestamp,
                reason=alert.reason,
                acknowledged=alert.acknowledged
            )
            for alert in alerts
        ]

    def acknowledge_alert(self, alert_id: int) -> AcknowledgeResponse:
        alert = self.alert_repo.get_by_id(alert_id)
        if not alert:
            raise AppError(message="Alert not found", status_code=404)
        updated_alert = self.alert_repo.mark_acknowledged(alert_id)
        return AcknowledgeResponse(
            id=updated_alert.id,
            acknowledged=updated_alert.acknowledged
        )

    def add_to_blacklist(self, plate_text: str, reason: str) -> BlacklistCreateResponse:
        norm_plate = self.normalize_plate(plate_text)
        entry = self.blacklist_repo.upsert(norm_plate, reason)
        return BlacklistCreateResponse(
            plate_text=entry.plate_text,
            reason=entry.reason,
            flagged_at=entry.flagged_at
        )
