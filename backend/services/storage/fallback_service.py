"""
Database Fallback Service

Implements graceful degradation when database is unavailable,
including circuit breaker pattern and retry logic with exponential backoff.
"""

import time
import logging
from typing import Dict, Any, Optional, List, Callable
from uuid import UUID
from datetime import datetime, UTC
from enum import Enum
from dataclasses import dataclass
from functools import wraps

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Circuit is open, failing fast
    HALF_OPEN = "half_open"  # Testing if service is back


@dataclass
class CircuitBreakerConfig:
    """Circuit breaker configuration."""
    failure_threshold: int = 5
    recovery_timeout: int = 60  # seconds
    success_threshold: int = 3
    timeout: int = 30  # seconds


@dataclass
class RetryConfig:
    """Retry configuration."""
    max_attempts: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True


class CircuitBreaker:
    """Circuit breaker implementation for database operations."""
    
    def __init__(self, config: CircuitBreakerConfig):
        """Initialize circuit breaker."""
        self.config = config
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.last_success_time = None
    
    def can_execute(self) -> bool:
        """Check if operation can be executed."""
        if self.state == CircuitState.CLOSED:
            return True
        elif self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        elif self.state == CircuitState.HALF_OPEN:
            return True
        
        return False
    
    def on_success(self):
        """Handle successful operation."""
        self.failure_count = 0
        self.last_success_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker closed - service recovered")
    
    def on_failure(self):
        """Handle failed operation."""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.success_count = 0
            logger.warning("Circuit breaker opened - service still failing")
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker opened after {self.failure_count} failures")
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        if self.last_failure_time is None:
            return True
        
        return (time.time() - self.last_failure_time) >= self.config.recovery_timeout


class RetryHandler:
    """Retry handler with exponential backoff."""
    
    def __init__(self, config: RetryConfig):
        """Initialize retry handler."""
        self.config = config
    
    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic."""
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Operation succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                
                if attempt < self.config.max_attempts - 1:
                    delay = self._calculate_delay(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    logger.error(f"All {self.config.max_attempts} attempts failed")
        
        raise last_exception
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt."""
        delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        delay = min(delay, self.config.max_delay)
        
        if self.config.jitter:
            # Add jitter to prevent thundering herd
            import random
            jitter = random.uniform(0.1, 0.3) * delay
            delay += jitter
        
        return delay


class InMemoryFallback:
    """In-memory fallback storage for when database is unavailable."""
    
    def __init__(self):
        """Initialize in-memory storage."""
        self.analyses: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, Dict[str, Any]] = {}
        self.biomarker_scores: Dict[str, List[Dict[str, Any]]] = {}
        self.clusters: Dict[str, List[Dict[str, Any]]] = {}
        self.insights: Dict[str, List[Dict[str, Any]]] = {}
        self.exports: Dict[str, Dict[str, Any]] = {}
        self.audit_logs: List[Dict[str, Any]] = []
        
        logger.info("In-memory fallback storage initialized")
    
    def save_analysis(self, analysis_dto: Dict[str, Any], user_id: UUID) -> Optional[UUID]:
        """Save analysis to in-memory storage."""
        try:
            analysis_id = analysis_dto.get("analysis_id")
            if not analysis_id:
                logger.error("Analysis ID is required for fallback storage")
                return None
            
            # Convert to string for consistent key usage
            analysis_id_str = str(analysis_id)
            
            # Store analysis data
            self.analyses[analysis_id_str] = {
                "id": analysis_id_str,
                "user_id": str(user_id),
                "status": analysis_dto.get("status", "completed"),
                "raw_biomarkers": analysis_dto.get("raw_biomarkers"),
                "questionnaire_data": analysis_dto.get("questionnaire_data"),
                "processing_time_seconds": analysis_dto.get("processing_time_seconds"),
                "analysis_version": analysis_dto.get("analysis_version", "1.0.0"),
                "pipeline_version": analysis_dto.get("pipeline_version", "1.0.0"),
                "created_at": datetime.now(UTC).isoformat(),
                "completed_at": datetime.now(UTC).isoformat() if analysis_dto.get("status") == "completed" else None
            }
            
            logger.info(f"Analysis {analysis_id_str} saved to fallback storage")
            self._log_audit_action("analysis_saved_fallback", "analysis", str(user_id), analysis_id_str)
            
            return analysis_id
            
        except Exception as e:
            logger.error(f"Error saving analysis to fallback storage: {str(e)}")
            return None
    
    def save_results(self, results_dto: Dict[str, Any], analysis_id: UUID) -> bool:
        """Save analysis results to in-memory storage."""
        try:
            analysis_id_str = str(analysis_id)
            
            # Store main result
            self.results[analysis_id_str] = {
                "biomarkers": results_dto.get("biomarkers"),
                "clusters": results_dto.get("clusters"),
                "insights": results_dto.get("insights"),
                "overall_score": results_dto.get("overall_score"),
                "risk_assessment": results_dto.get("risk_assessment"),
                "recommendations": results_dto.get("recommendations"),
                "result_version": results_dto.get("result_version", "1.0.0"),
                "confidence_score": results_dto.get("confidence_score"),
                "processing_metadata": results_dto.get("processing_metadata"),
                "created_at": datetime.now(UTC).isoformat()
            }
            
            # Store individual components
            biomarkers = results_dto.get("biomarkers", [])
            if biomarkers:
                self.biomarker_scores[analysis_id_str] = biomarkers
            
            clusters = results_dto.get("clusters", [])
            if clusters:
                self.clusters[analysis_id_str] = clusters
            
            insights = results_dto.get("insights", [])
            if insights:
                self.insights[analysis_id_str] = insights
            
            logger.info(f"Results for analysis {analysis_id_str} saved to fallback storage")
            self._log_audit_action("results_saved_fallback", "analysis_result", None, analysis_id_str)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving results to fallback storage: {str(e)}")
            return False
    
    def get_analysis_result(self, analysis_id: UUID) -> Optional[Dict[str, Any]]:
        """Get analysis result from in-memory storage."""
        try:
            analysis_id_str = str(analysis_id)
            
            # Check if analysis exists
            if analysis_id_str not in self.analyses:
                logger.warning(f"Analysis {analysis_id_str} not found in fallback storage")
                return None
            
            # Get result data
            result = self.results.get(analysis_id_str, {})
            biomarkers = self.biomarker_scores.get(analysis_id_str, [])
            clusters = self.clusters.get(analysis_id_str, [])
            insights = self.insights.get(analysis_id_str, [])
            
            return {
                "analysis_id": analysis_id_str,
                "result_version": result.get("result_version", "1.0.0"),
                "biomarkers": biomarkers,
                "clusters": clusters,
                "insights": insights,
                "recommendations": result.get("recommendations", []),
                "overall_score": result.get("overall_score"),
                "meta": {
                    "confidence_score": result.get("confidence_score"),
                    "processing_metadata": result.get("processing_metadata"),
                    "fallback_storage": True  # Indicate this came from fallback
                },
                "created_at": result.get("created_at", datetime.now(UTC).isoformat())
            }
            
        except Exception as e:
            logger.error(f"Error getting analysis result from fallback storage: {str(e)}")
            return None
    
    def get_analysis_history(self, user_id: UUID, limit: int = 10) -> List[Dict[str, Any]]:
        """Get analysis history from in-memory storage."""
        try:
            user_id_str = str(user_id)
            user_analyses = [
                analysis for analysis in self.analyses.values()
                if analysis.get("user_id") == user_id_str
            ]
            
            # Sort by created_at descending and limit
            user_analyses.sort(key=lambda x: x.get("created_at", ""), reverse=True)
            return user_analyses[:limit]
            
        except Exception as e:
            logger.error(f"Error getting analysis history from fallback storage: {str(e)}")
            return []
    
    def _log_audit_action(self, action: str, resource_type: str, user_id: str = None, 
                         resource_id: str = None, details: Dict[str, Any] = None):
        """Log action to in-memory audit trail."""
        try:
            audit_log = {
                "action": action,
                "resource_type": resource_type,
                "user_id": user_id,
                "resource_id": resource_id,
                "details": details or {},
                "severity": "info",
                "outcome": "success",
                "created_at": datetime.now(UTC).isoformat(),
                "fallback_storage": True
            }
            self.audit_logs.append(audit_log)
        except Exception as e:
            logger.error(f"Failed to log audit action {action}: {str(e)}")


class DatabaseFallbackService:
    """Service that provides fallback capabilities for database operations."""
    
    def __init__(self, primary_service, circuit_config: CircuitBreakerConfig = None, 
                 retry_config: RetryConfig = None):
        """Initialize fallback service."""
        self.primary_service = primary_service
        self.circuit_breaker = CircuitBreaker(circuit_config or CircuitBreakerConfig())
        self.retry_handler = RetryHandler(retry_config or RetryConfig())
        self.fallback_storage = InMemoryFallback()
        
        logger.info("Database fallback service initialized")
    
    def execute_with_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Execute database operation with fallback support."""
        if not self.circuit_breaker.can_execute():
            logger.warning(f"Circuit breaker is open, using fallback for {operation}")
            return self._execute_fallback(operation, *args, **kwargs)
        
        try:
            # Attempt primary operation with retry
            result = self.retry_handler.execute_with_retry(
                getattr(self.primary_service, operation),
                *args, **kwargs
            )
            
            self.circuit_breaker.on_success()
            logger.debug(f"Primary operation {operation} succeeded")
            return result
            
        except Exception as e:
            self.circuit_breaker.on_failure()
            logger.warning(f"Primary operation {operation} failed: {str(e)}")
            logger.info(f"Falling back to in-memory storage for {operation}")
            
            return self._execute_fallback(operation, *args, **kwargs)
    
    def _execute_fallback(self, operation: str, *args, **kwargs) -> Any:
        """Execute operation using fallback storage."""
        try:
            if operation == "save_analysis":
                return self.fallback_storage.save_analysis(*args, **kwargs)
            elif operation == "save_results":
                return self.fallback_storage.save_results(*args, **kwargs)
            elif operation == "get_analysis_result":
                return self.fallback_storage.get_analysis_result(*args, **kwargs)
            elif operation == "get_analysis_history":
                return self.fallback_storage.get_analysis_history(*args, **kwargs)
            else:
                logger.error(f"Fallback operation {operation} not supported")
                return None
                
        except Exception as e:
            logger.error(f"Fallback operation {operation} failed: {str(e)}")
            return None
    
    def get_circuit_breaker_status(self) -> Dict[str, Any]:
        """Get current circuit breaker status."""
        return {
            "state": self.circuit_breaker.state.value,
            "failure_count": self.circuit_breaker.failure_count,
            "success_count": self.circuit_breaker.success_count,
            "last_failure_time": self.circuit_breaker.last_failure_time,
            "last_success_time": self.circuit_breaker.last_success_time
        }
    
    def reset_circuit_breaker(self):
        """Reset circuit breaker to closed state."""
        self.circuit_breaker.state = CircuitState.CLOSED
        self.circuit_breaker.failure_count = 0
        self.circuit_breaker.success_count = 0
        logger.info("Circuit breaker reset to closed state")


def fallback_decorator(operation_name: str):
    """Decorator that tries the primary function, then falls back on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                # Try the primary persistence operation
                return func(self, *args, **kwargs)
            except Exception as e:
                # Log and trigger fallback path once
                if hasattr(self, "fallback_service"):
                    logger.warning(
                        f"Primary operation {operation_name} failed: {e}. "
                        "Switching to fallback service."
                    )
                    return self.fallback_service.execute_with_fallback(
                        operation_name, *args, **kwargs
                    )
                raise
        return wrapper
    return decorator

