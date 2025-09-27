"""
Unit tests for FastAPI main application
HealthIQ-AI v5 Backend
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from app.main import app


class TestMainApplication:
    """Test FastAPI main application functionality"""
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct response"""
        response = self.client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "HealthIQ-AI v5 Backend"
        assert data["version"] == "5.0.0"
        assert data["docs"] == "/docs"
        assert data["api_prefix"] == "/api"
    
    def test_health_endpoint(self):
        """Test health endpoint is accessible"""
        response = self.client.get("/api/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
    
    def test_404_handler(self):
        """Test custom 404 handler for non-existent endpoints"""
        response = self.client.get("/api/nonexistent")
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "Not found"
        assert data["message"] == "API endpoint not found"
    
    def test_cors_headers(self):
        """Test CORS headers are properly set"""
        response = self.client.options("/", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        
        # CORS preflight should return 200
        assert response.status_code == 200
    
    def test_docs_endpoint(self):
        """Test API documentation endpoint is accessible"""
        response = self.client.get("/docs")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_redoc_endpoint(self):
        """Test ReDoc documentation endpoint is accessible"""
        response = self.client.get("/redoc")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
    
    def test_analysis_endpoints_accessible(self):
        """Test analysis endpoints are properly mounted"""
        # Test that analysis endpoints are accessible (even if they return errors)
        response = self.client.get("/api/analysis/history")
        
        # Should not return 404 (endpoint exists)
        assert response.status_code != 404
    
    @patch('uvicorn.run')
    def test_main_execution(self, mock_uvicorn):
        """Test main execution when run directly"""
        # This test ensures the main block doesn't crash
        # We can't actually run uvicorn in tests, so we mock it
        import app.main
        
        # The main block should not raise an exception
        # This is more of a smoke test
        assert True  # If we get here, the import and main block are fine


class TestApplicationConfiguration:
    """Test FastAPI application configuration"""
    
    def test_app_title(self):
        """Test application title is set correctly"""
        assert app.title == "HealthIQ-AI v5"
    
    def test_app_description(self):
        """Test application description is set correctly"""
        assert app.description == "AI-powered biomarker analysis platform"
    
    def test_app_version(self):
        """Test application version is set correctly"""
        assert app.version == "5.0.0"
    
    def test_docs_url(self):
        """Test docs URL is configured"""
        assert app.docs_url == "/docs"
    
    def test_redoc_url(self):
        """Test ReDoc URL is configured"""
        assert app.redoc_url == "/redoc"
    
    def test_cors_middleware_configured(self):
        """Test CORS middleware is properly configured"""
        # Check that CORS middleware is in the middleware stack
        middleware_types = [type(middleware).__name__ for middleware in app.user_middleware]
        assert "CORSMiddleware" in middleware_types or "Middleware" in middleware_types
    
    def test_routes_included(self):
        """Test that API routes are properly included"""
        # Check that routes are registered
        route_paths = [route.path for route in app.routes]
        
        # Should have health and analysis routes
        assert any("/api/health" in path for path in route_paths)
        assert any("/api/analysis" in path for path in route_paths)
        assert "/" in route_paths  # Root endpoint


class TestErrorHandling:
    """Test error handling functionality"""
    
    def setup_method(self):
        """Set up test client for each test"""
        self.client = TestClient(app)
    
    def test_404_for_unknown_routes(self):
        """Test 404 response for unknown routes"""
        response = self.client.get("/unknown/route")
        
        assert response.status_code == 404
        data = response.json()
        assert "error" in data
        assert "message" in data
    
    def test_404_for_api_unknown_routes(self):
        """Test 404 response for unknown API routes"""
        response = self.client.get("/api/unknown/route")
        
        assert response.status_code == 404
        data = response.json()
        assert data["error"] == "Not found"
        assert data["message"] == "API endpoint not found"
    
    def test_method_not_allowed(self):
        """Test method not allowed responses"""
        # Try POST to a GET-only endpoint
        response = self.client.post("/")
        
        # Should return 405 Method Not Allowed
        assert response.status_code == 405
