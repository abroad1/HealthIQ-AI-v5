"""
Fallback Service Integration Tests

Tests database fallback mechanisms, circuit breaker pattern, and retry logic.
These tests validate that the system gracefully handles database outages.
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from services.storage.fallback_service import (
    CircuitBreaker, CircuitState, CircuitBreakerConfig,
    RetryHandler, RetryConfig, InMemoryFallback, DatabaseFallbackService
)
from services.storage.persistence_service import PersistenceService


class TestCircuitBreaker:
    """Test circuit breaker functionality."""
    
    def test_circuit_breaker_initial_state(self):
        """Test circuit breaker starts in closed state."""
        config = CircuitBreakerConfig()
        breaker = CircuitBreaker(config)
        
        assert breaker.state == CircuitState.CLOSED
        assert breaker.failure_count == 0
        assert breaker.can_execute() is True
    
    def test_circuit_breaker_failure_threshold(self):
        """Test circuit breaker opens after failure threshold."""
        config = CircuitBreakerConfig(failure_threshold=3)
        breaker = CircuitBreaker(config)

        # 1st failure - still CLOSED
        breaker.on_failure()
        assert breaker.state == CircuitState.CLOSED
        # 2nd failure - still CLOSED
        breaker.on_failure()
        assert breaker.state == CircuitState.CLOSED
        # 3rd failure - opens circuit
        breaker.on_failure()
        assert breaker.state == CircuitState.OPEN
        assert breaker.can_execute() is False
    
    def test_circuit_breaker_recovery(self):
        """Test circuit breaker recovery after timeout."""
        config = CircuitBreakerConfig(recovery_timeout=1)  # 1 second timeout
        breaker = CircuitBreaker(config)
        
        # Open circuit
        for i in range(config.failure_threshold + 1):
            breaker.on_failure()
        assert breaker.state == CircuitState.OPEN
        
        # Wait for recovery timeout
        time.sleep(1.1)
        
        # Should be able to execute (half-open)
        assert breaker.can_execute() is True
        assert breaker.state == CircuitState.HALF_OPEN
    
    def test_circuit_breaker_success_recovery(self):
        """Test circuit breaker closes after successful operations."""
        config = CircuitBreakerConfig(success_threshold=2)
        breaker = CircuitBreaker(config)
        
        # Open circuit
        for i in range(config.failure_threshold + 1):
            breaker.on_failure()
        assert breaker.state == CircuitState.OPEN
        
        # Wait for recovery and simulate half-open
        time.sleep(1.1)
        breaker.state = CircuitState.HALF_OPEN
        
        # Simulate successful operations
        for i in range(config.success_threshold):
            breaker.on_success()
        
        assert breaker.state == CircuitState.CLOSED
        assert breaker.success_count == 0


class TestRetryHandler:
    """Test retry logic with exponential backoff."""
    
    def test_retry_handler_success_first_attempt(self):
        """Test retry handler succeeds on first attempt."""
        config = RetryConfig(max_attempts=3)
        handler = RetryHandler(config)
        
        def successful_operation():
            return "success"
        
        result = handler.execute_with_retry(successful_operation)
        assert result == "success"
    
    def test_retry_handler_retry_on_failure(self):
        """Test retry handler retries on failure."""
        config = RetryConfig(max_attempts=3, base_delay=0.1)
        handler = RetryHandler(config)
        
        attempt_count = 0
        
        def failing_operation():
            nonlocal attempt_count
            attempt_count += 1
            if attempt_count < 3:
                raise Exception(f"Attempt {attempt_count} failed")
            return "success"
        
        result = handler.execute_with_retry(failing_operation)
        assert result == "success"
        assert attempt_count == 3
    
    def test_retry_handler_max_attempts_exceeded(self):
        """Test retry handler fails after max attempts."""
        config = RetryConfig(max_attempts=2, base_delay=0.1)
        handler = RetryHandler(config)
        
        def always_failing_operation():
            raise Exception("Always fails")
        
        with pytest.raises(Exception, match="Always fails"):
            handler.execute_with_retry(always_failing_operation)
    
    def test_retry_handler_exponential_backoff(self):
        """Test exponential backoff calculation."""
        config = RetryConfig(base_delay=1.0, exponential_base=2.0, jitter=False)
        handler = RetryHandler(config)
        
        # Test delay calculation
        delay1 = handler._calculate_delay(0)  # First retry
        delay2 = handler._calculate_delay(1)  # Second retry
        delay3 = handler._calculate_delay(2)  # Third retry
        
        assert delay1 == 1.0
        assert delay2 == 2.0
        assert delay3 == 4.0


class TestInMemoryFallback:
    """Test in-memory fallback storage."""
    
    def test_fallback_storage_initialization(self):
        """Test fallback storage initializes correctly."""
        storage = InMemoryFallback()
        
        assert storage.analyses == {}
        assert storage.results == {}
        assert storage.biomarker_scores == {}
        assert storage.clusters == {}
        assert storage.insights == {}
        assert storage.exports == {}
        assert storage.audit_logs == []
    
    def test_save_analysis_fallback(self):
        """Test saving analysis to fallback storage."""
        storage = InMemoryFallback()
        user_id = uuid4()
        analysis_id = uuid4()
        
        analysis_dto = {
            "analysis_id": str(analysis_id),
            "status": "completed",
            "raw_biomarkers": {"glucose": 100},
            "processing_time_seconds": 5.0
        }
        
        result = storage.save_analysis(analysis_dto, user_id)

        # save_analysis returns str(analysis_id) from dto
        assert result == str(analysis_id)
        assert str(analysis_id) in storage.analyses
        assert storage.analyses[str(analysis_id)]["user_id"] == str(user_id)
        assert storage.analyses[str(analysis_id)]["status"] == "completed"
    
    def test_save_results_fallback(self):
        """Test saving results to fallback storage."""
        storage = InMemoryFallback()
        analysis_id = uuid4()
        
        results_dto = {
            "biomarkers": [{"name": "glucose", "value": 100}],
            "clusters": [{"name": "metabolic", "score": 0.8}],
            "insights": [{"title": "Test insight", "content": "Test content"}],
            "overall_score": 0.75
        }
        
        result = storage.save_results(results_dto, analysis_id)
        
        assert result is True
        assert str(analysis_id) in storage.results
        assert str(analysis_id) in storage.biomarker_scores
        assert str(analysis_id) in storage.clusters
        assert str(analysis_id) in storage.insights
    
    def test_get_analysis_result_fallback(self):
        """Test getting analysis result from fallback storage."""
        storage = InMemoryFallback()
        analysis_id = uuid4()

        storage.save_analysis(
            {"analysis_id": str(analysis_id), "status": "completed"},
            analysis_id
        )

        # Save some data first
        results_dto = {
            "biomarkers": [{"name": "glucose", "value": 100}],
            "overall_score": 0.75
        }
        storage.save_results(results_dto, analysis_id)
        
        result = storage.get_analysis_result(analysis_id)
        
        assert result is not None
        assert result["analysis_id"] == str(analysis_id)
        assert result["biomarkers"] == [{"name": "glucose", "value": 100}]
        assert result["overall_score"] == 0.75
        assert result["meta"]["fallback_storage"] is True
    
    def test_get_analysis_history_fallback(self):
        """Test getting analysis history from fallback storage."""
        storage = InMemoryFallback()
        user_id = uuid4()
        
        # Save multiple analyses
        for i in range(3):
            analysis_id = uuid4()
            analysis_dto = {
                "analysis_id": str(analysis_id),
                "status": "completed"
            }
            storage.save_analysis(analysis_dto, user_id)
        
        history = storage.get_analysis_history(user_id)
        
        assert len(history) == 3
        assert all(h["user_id"] == str(user_id) for h in history)


class TestDatabaseFallbackService:
    """Test database fallback service integration."""
    
    def test_fallback_service_initialization(self):
        """Test fallback service initializes correctly."""
        mock_primary = MagicMock()
        service = DatabaseFallbackService(mock_primary)
        
        assert service.primary_service == mock_primary
        assert service.circuit_breaker is not None
        assert service.retry_handler is not None
        assert service.fallback_storage is not None
    
    def test_execute_with_fallback_success(self):
        """Test fallback service executes primary operation successfully."""
        mock_primary = MagicMock()
        mock_primary.test_operation.return_value = "success"
        
        service = DatabaseFallbackService(mock_primary)
        
        result = service.execute_with_fallback("test_operation", "arg1", "arg2")
        
        assert result == "success"
        mock_primary.test_operation.assert_called_once_with("arg1", "arg2")
    
    def test_execute_with_fallback_circuit_open(self):
        """Test fallback service uses fallback when circuit is open."""
        mock_primary = MagicMock()
        service = DatabaseFallbackService(mock_primary)
        
        # Open circuit breaker
        for i in range(service.circuit_breaker.config.failure_threshold + 1):
            service.circuit_breaker.on_failure()
        
        # Mock fallback storage
        service.fallback_storage.save_analysis = MagicMock(return_value="fallback_result")
        
        result = service.execute_with_fallback("save_analysis", {"test": "data"}, uuid4())
        
        assert result == "fallback_result"
        mock_primary.save_analysis.assert_not_called()
    
    def test_execute_with_fallback_primary_failure(self):
        """Test fallback service uses fallback when primary fails after retries."""
        mock_primary = MagicMock()
        mock_primary.save_analysis.side_effect = SQLAlchemyError("Database error")

        service = DatabaseFallbackService(mock_primary)
        service.fallback_storage.save_analysis = MagicMock(return_value="fallback_result")

        result = service.execute_with_fallback("save_analysis", {"test": "data"}, uuid4())

        assert result == "fallback_result"
        # RetryConfig default max_attempts=3; primary called 3 times before fallback
        assert mock_primary.save_analysis.call_count == 3
    
    def test_circuit_breaker_status(self):
        """Test circuit breaker status reporting."""
        service = DatabaseFallbackService(MagicMock())
        
        status = service.get_circuit_breaker_status()
        
        assert "state" in status
        assert "failure_count" in status
        assert "success_count" in status
        assert status["state"] == CircuitState.CLOSED.value
    
    def test_circuit_breaker_reset(self):
        """Test circuit breaker reset functionality."""
        service = DatabaseFallbackService(MagicMock())
        
        # Open circuit
        for i in range(service.circuit_breaker.config.failure_threshold + 1):
            service.circuit_breaker.on_failure()
        
        assert service.circuit_breaker.state == CircuitState.OPEN
        
        # Reset circuit
        service.reset_circuit_breaker()
        
        assert service.circuit_breaker.state == CircuitState.CLOSED
        assert service.circuit_breaker.failure_count == 0


class TestPersistenceServiceFallback:
    """Test persistence service with fallback integration."""
    
    def test_persistence_service_with_fallback(self, db_session):
        """Test persistence service initializes with fallback enabled."""
        service = PersistenceService(db_session, enable_fallback=True)
        
        assert service.fallback_service is not None
        assert hasattr(service, 'get_fallback_status')
        assert hasattr(service, 'reset_fallback_circuit_breaker')
    
    def test_persistence_service_without_fallback(self, db_session):
        """Test persistence service initializes without fallback."""
        service = PersistenceService(db_session, enable_fallback=False)
        
        assert service.fallback_service is None
    
    def test_fallback_status_reporting(self, db_session):
        """Test fallback status reporting."""
        service = PersistenceService(db_session, enable_fallback=True)
        
        status = service.get_fallback_status()
        
        assert status is not None
        assert "state" in status
        assert "failure_count" in status
    
    def test_database_availability_check(self, db_session):
        """Test database availability checking."""
        service = PersistenceService(db_session, enable_fallback=True)
        
        is_available = service.is_database_available()
        
        assert isinstance(is_available, bool)
    
    def test_fallback_decorator_integration(self, db_session):
        """Test that fallback decorator works: primary fails -> fallback used."""
        service = PersistenceService(db_session, enable_fallback=True)

        # Correct attribute: fallback_service.fallback_storage (not service.fallback_storage)
        service.fallback_service.fallback_storage.save_analysis = MagicMock(return_value="fallback_result")

        # Make primary fail so decorator triggers fallback
        with patch.object(service.analysis_repo, 'upsert_by_analysis_id', side_effect=SQLAlchemyError("Database error")):
            result = service.save_analysis(
                {"analysis_id": str(uuid4()), "status": "completed"},
                uuid4()
            )

        assert result == "fallback_result"
