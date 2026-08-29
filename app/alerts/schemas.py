from datetime import datetime
from pydantic import BaseModel, Field, field_serializer
from app.core.time import format_utc_iso

class TrajectorySighting(BaseModel):
    camera_id: str
    location_name: str
    gps_lat: float
    gps_lng: float
    timestamp: datetime
    direction_from_prev: str | None = None
    speed_from_prev_kmh: float | None = None

    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info) -> str:
        return format_utc_iso(dt)

class TrajectoryResult(BaseModel):
    found: bool
    sightings: list[TrajectorySighting]

class AlertSearchResponse(BaseModel):
    plate: str
    blacklisted: bool
    reason: str | None = None
    flagged_at: datetime | None = None
    trajectory: TrajectoryResult

    @field_serializer('flagged_at')
    def serialize_flagged_at(self, dt: datetime | None, _info) -> str | None:
        return format_utc_iso(dt)

class AlertFeedItem(BaseModel):
    id: int
    plate_text: str
    camera_id: str
    location_name: str
    timestamp: datetime
    reason: str
    acknowledged: bool

    @field_serializer('timestamp')
    def serialize_timestamp(self, dt: datetime, _info) -> str:
        return format_utc_iso(dt)

class AcknowledgeResponse(BaseModel):
    id: int
    acknowledged: bool

class BlacklistCreateRequest(BaseModel):
    plate_text: str
    reason: str

class BlacklistCreateResponse(BaseModel):
    plate_text: str
    reason: str
    flagged_at: datetime

    @field_serializer('flagged_at')
    def serialize_flagged_at(self, dt: datetime, _info) -> str:
        return format_utc_iso(dt)
