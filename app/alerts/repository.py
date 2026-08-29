from datetime import datetime
from sqlalchemy.orm import Session
from app.alerts.models import Blacklist, Alert
from app.core.time import utc_now

class BlacklistRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_plate(self, plate: str) -> Blacklist | None:
        return self.db.query(Blacklist).filter(Blacklist.plate_text == plate).first()

    def upsert(self, plate_text: str, reason: str) -> Blacklist:
        # ASSUMPTION: Upsert updates existing entry's reason and flagged_at timestamp if plate already exists.
        entry = self.get_by_plate(plate_text)
        if entry:
            entry.reason = reason
            entry.flagged_at = utc_now()
        else:
            entry = Blacklist(
                plate_text=plate_text,
                reason=reason,
                flagged_at=utc_now()
            )
            self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)
        return entry

class AlertRepository:
    def __init__(self, db: Session):
        self.db = db

    def list(self, limit: int = 20, unacknowledged_only: bool = False) -> list[Alert]:
        query = self.db.query(Alert)
        if unacknowledged_only:
            query = query.filter(Alert.acknowledged.is_(False))
        return query.order_by(Alert.timestamp.desc()).limit(limit).all()

    def get_by_id(self, alert_id: int) -> Alert | None:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def create(
        self,
        plate_text: str,
        camera_id: str,
        location_name: str,
        timestamp: datetime,
        reason: str,
        acknowledged: bool = False
    ) -> Alert:
        alert = Alert(
            plate_text=plate_text,
            camera_id=camera_id,
            location_name=location_name,
            timestamp=timestamp,
            reason=reason,
            acknowledged=acknowledged
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def mark_acknowledged(self, alert_id: int) -> Alert | None:
        alert = self.get_by_id(alert_id)
        if alert:
            alert.acknowledged = True
            self.db.commit()
            self.db.refresh(alert)
        return alert
