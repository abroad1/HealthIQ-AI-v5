"""
WEDGE-METRICS-B — first-party wedge event ingestion (no Intelligence Core changes).

Lives under unit tests to avoid integration/conftest DB migration (endpoint is stateless).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_wedge_events_valid_returns_204(client: TestClient) -> None:
    response = client.post(
        "/api/wedge-events",
        json={
            "event_name": "wedge_auth_login_success",
            "timestamp": "2026-04-11T12:00:00.000Z",
            "env": "development",
            "route": "/login",
        },
    )
    assert response.status_code == 204
    assert response.content == b""


def test_wedge_events_rejects_unknown_event_name(client: TestClient) -> None:
    response = client.post(
        "/api/wedge-events",
        json={
            "event_name": "wedge_paid_conversion",
            "timestamp": "2026-04-11T12:00:00.000Z",
            "env": "development",
        },
    )
    assert response.status_code == 422


def test_wedge_events_rejects_deferred_pdf_event(client: TestClient) -> None:
    response = client.post(
        "/api/wedge-events",
        json={
            "event_name": "wedge_clinician_report_pdf_downloaded",
            "timestamp": "2026-04-11T12:00:00.000Z",
            "env": "development",
        },
    )
    assert response.status_code == 422
