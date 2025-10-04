import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_export_route_rejects_unsupported_format(monkeypatch):
    r = client.post("/api/analysis/export", json={"analysis_id":"00000000-0000-0000-0000-000000000000","format":"PDF"})
    assert r.status_code == 400

# Add a happy-path test once AnalysisRepository.get_result_dto is available and storage is mocked.
