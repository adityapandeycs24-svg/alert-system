from datetime import datetime, timezone
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app
from app.alerts.router import get_trajectory_provider
from app.alerts.schemas import TrajectoryResult, TrajectorySighting

class FakeTrajectoryProvider:
    def __init__(self, canned_result: TrajectoryResult | None = None):
        self.canned_result = canned_result or TrajectoryResult(found=False, sightings=[])

    def get_trajectory(self, plate: str) -> TrajectoryResult:
        return self.canned_result

from sqlalchemy.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    def override_get_trajectory_provider():
        return FakeTrajectoryProvider()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_trajectory_provider] = override_get_trajectory_provider

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
