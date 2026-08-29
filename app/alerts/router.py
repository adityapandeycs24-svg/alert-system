from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.alerts.interfaces import TrajectoryProvider, StubTrajectoryProvider
from app.alerts.service import AlertService
from app.alerts.schemas import (
    AlertSearchResponse,
    AlertFeedItem,
    AcknowledgeResponse,
    BlacklistCreateRequest,
    BlacklistCreateResponse,
)

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

def get_trajectory_provider() -> TrajectoryProvider:
    """Dependency provider for TrajectoryProvider. Defaults to StubTrajectoryProvider."""
    return StubTrajectoryProvider()

def get_alert_service(
    db: Session = Depends(get_db),
    trajectory_provider: TrajectoryProvider = Depends(get_trajectory_provider),
) -> AlertService:
    return AlertService(db=db, trajectory_provider=trajectory_provider)

@router.get("/search/{plate}", response_model=AlertSearchResponse, status_code=status.HTTP_200_OK)
def search_plate(
    plate: str,
    service: AlertService = Depends(get_alert_service),
):
    return service.search_plate(plate)

@router.get("/feed", response_model=list[AlertFeedItem], status_code=status.HTTP_200_OK)
def get_feed(
    limit: int = Query(default=20, ge=1),
    unacknowledged_only: bool = Query(default=False),
    service: AlertService = Depends(get_alert_service),
):
    return service.get_feed(limit=limit, unacknowledged_only=unacknowledged_only)

@router.post("/feed/{alert_id}/acknowledge", response_model=AcknowledgeResponse, status_code=status.HTTP_200_OK)
def acknowledge_alert(
    alert_id: int,
    service: AlertService = Depends(get_alert_service),
):
    return service.acknowledge_alert(alert_id)

@router.post("/blacklist", response_model=BlacklistCreateResponse, status_code=status.HTTP_201_CREATED)
def add_to_blacklist(
    request: BlacklistCreateRequest,
    service: AlertService = Depends(get_alert_service),
):
    return service.add_to_blacklist(plate_text=request.plate_text, reason=request.reason)
