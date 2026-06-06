"""
Tests for the FastAPI application
"""

import pytest


class TestRootEndpoint:
    """Tests for the root endpoint"""
    
    def test_root_endpoint_returns_json(self, test_client):
        """Test that the root endpoint returns valid JSON"""
        response = test_client.get("/")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
    
    def test_root_endpoint_structure(self, test_client):
        """Test that the root endpoint returns expected structure"""
        response = test_client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data
        
        assert data["name"] == "Bazov API"
        assert data["version"] == "0.1.0"
        assert data["docs"] == "/docs"
        assert data["health"] == "/api/v1/health"


class TestHealthEndpoint:
    """Tests for the health check endpoint"""
    
    def test_health_endpoint(self, test_client):
        """Test that the health endpoint returns healthy status"""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data


class TestAPIV1Health:
    """Tests for the v1 health endpoint"""
    
    def test_v1_health_endpoint(self, test_client):
        """Test that the v1 health endpoint works"""
        response = test_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "version" in data
        assert "app_name" in data
        assert "debug" in data
