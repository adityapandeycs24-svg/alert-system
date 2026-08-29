from sqlalchemy import Column, Integer, String, DateTime, Boolean
from app.database import Base
from app.core.time import utc_now

class Blacklist(Base):
    __tablename__ = "blacklists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate_text = Column(String, unique=True, index=True, nullable=False)
    reason = Column(String, nullable=False)
    flagged_at = Column(DateTime(timezone=True), nullable=False, default=utc_now)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    plate_text = Column(String, nullable=False)
    camera_id = Column(String, nullable=False)
    location_name = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    reason = Column(String, nullable=False)
    acknowledged = Column(Boolean, default=False, nullable=False)
