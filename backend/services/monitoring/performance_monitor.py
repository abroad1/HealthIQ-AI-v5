"""
Performance Monitoring Service

Monitors database performance, connection pool health, and query execution times.
"""

import time
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, UTC
from dataclasses import dataclass, field
from collections import defaultdict, deque
from sqlalchemy import event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


@dataclass
class QueryMetrics:
    """Query performance metrics."""
    query: str
    execution_time: float
    timestamp: datetime
    parameters: Dict[str, Any] = field(default_factory=dict)
    rows_affected: int = 0
    error: Optional[str] = None


@dataclass
class ConnectionMetrics:
    """Connection pool metrics."""
    pool_size: int
    checked_in: int
    checked_out: int
    overflow: int
    invalid: int
    timestamp: datetime


@dataclass
class PerformanceSummary:
    """Performance summary statistics."""
    total_queries: int
    avg_execution_time: float
    max_execution_time: float
    min_execution_time: float
    error_rate: float
    slow_queries: int
    timestamp: datetime


class PerformanceMonitor:
    """Monitors database performance and connection health."""
    
    def __init__(self, max_query_history: int = 1000, slow_query_threshold: float = 1.0):
        """
        Initialize performance monitor.
        
        Args:
            max_query_history: Maximum number of queries to keep in history
            slow_query_threshold: Threshold in seconds for slow queries
        """
        self.max_query_history = max_query_history
        self.slow_query_threshold = slow_query_threshold
        
        # Query metrics storage
        self.query_history: deque = deque(maxlen=max_query_history)
        self.query_stats: Dict[str, List[float]] = defaultdict(list)
        
        # Connection metrics storage
        self.connection_history: deque = deque(maxlen=100)
        
        # Performance counters
        self.total_queries = 0
        self.total_errors = 0
        self.slow_queries = 0
        
        logger.info("Performance monitor initialized")
    
    def start_monitoring(self, engine: Engine):
        """Start monitoring database engine."""
        # Add event listeners for query monitoring
        event.listen(engine, "before_cursor_execute", self._before_cursor_execute)
        event.listen(engine, "after_cursor_execute", self._after_cursor_execute)
        event.listen(engine, "handle_error", self._handle_error)
        
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self, engine: Engine):
        """Stop monitoring database engine."""
        # Remove event listeners
        event.remove(engine, "before_cursor_execute", self._before_cursor_execute)
        event.remove(engine, "after_cursor_execute", self._after_cursor_execute)
        event.remove(engine, "handle_error", self._handle_error)
        
        logger.info("Performance monitoring stopped")
    
    def _before_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        """Record query start time."""
        context._query_start_time = time.time()
        context._query_statement = statement
        context._query_parameters = parameters
    
    def _after_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        """Record query completion metrics."""
        if hasattr(context, '_query_start_time'):
            execution_time = time.time() - context._query_start_time
            
            # Create query metrics
            query_metrics = QueryMetrics(
                query=statement,
                execution_time=execution_time,
                timestamp=datetime.now(UTC),
                parameters=parameters or {},
                rows_affected=cursor.rowcount if hasattr(cursor, 'rowcount') else 0
            )
            
            # Store metrics
            self.query_history.append(query_metrics)
            self.query_stats[statement].append(execution_time)
            
            # Update counters
            self.total_queries += 1
            if execution_time > self.slow_query_threshold:
                self.slow_queries += 1
                logger.warning(f"Slow query detected: {execution_time:.3f}s - {statement[:100]}...")
            
            # Log performance metrics
            logger.debug(f"Query executed in {execution_time:.3f}s: {statement[:100]}...")
    
    def _handle_error(self, conn, cursor, statement, parameters, context, executemany, exception):
        """Record query error."""
        self.total_errors += 1
        
        if hasattr(context, '_query_start_time'):
            execution_time = time.time() - context._query_start_time
            
            query_metrics = QueryMetrics(
                query=statement,
                execution_time=execution_time,
                timestamp=datetime.now(UTC),
                parameters=parameters or {},
                error=str(exception)
            )
            
            self.query_history.append(query_metrics)
            logger.error(f"Query error after {execution_time:.3f}s: {str(exception)}")
    
    def record_connection_metrics(self, pool_status: Dict[str, int]):
        """Record connection pool metrics."""
        connection_metrics = ConnectionMetrics(
            pool_size=pool_status.get("pool_size", 0),
            checked_in=pool_status.get("checked_in", 0),
            checked_out=pool_status.get("checked_out", 0),
            overflow=pool_status.get("overflow", 0),
            invalid=pool_status.get("invalid", 0),
            timestamp=datetime.now(UTC)
        )
        
        self.connection_history.append(connection_metrics)
        logger.debug(f"Connection metrics recorded: {pool_status}")
    
    def get_query_performance_summary(self) -> PerformanceSummary:
        """Get performance summary for all queries."""
        if not self.query_history:
            return PerformanceSummary(
                total_queries=0,
                avg_execution_time=0.0,
                max_execution_time=0.0,
                min_execution_time=0.0,
                error_rate=0.0,
                slow_queries=0,
                timestamp=datetime.now(UTC)
            )
        
        execution_times = [q.execution_time for q in self.query_history if q.error is None]
        error_count = sum(1 for q in self.query_history if q.error is not None)
        
        if execution_times:
            avg_time = sum(execution_times) / len(execution_times)
            max_time = max(execution_times)
            min_time = min(execution_times)
        else:
            avg_time = max_time = min_time = 0.0
        
        error_rate = (error_count / len(self.query_history)) * 100 if self.query_history else 0.0
        
        return PerformanceSummary(
            total_queries=len(self.query_history),
            avg_execution_time=avg_time,
            max_execution_time=max_time,
            min_execution_time=min_time,
            error_rate=error_rate,
            slow_queries=self.slow_queries,
            timestamp=datetime.now(UTC)
        )
    
    def get_slow_queries(self, limit: int = 10) -> List[QueryMetrics]:
        """Get slowest queries."""
        slow_queries = [q for q in self.query_history if q.execution_time > self.slow_query_threshold]
        return sorted(slow_queries, key=lambda x: x.execution_time, reverse=True)[:limit]
    
    def get_query_stats_by_statement(self) -> Dict[str, Dict[str, float]]:
        """Get statistics grouped by SQL statement."""
        stats = {}
        
        for statement, times in self.query_stats.items():
            if times:
                stats[statement] = {
                    "count": len(times),
                    "avg_time": sum(times) / len(times),
                    "max_time": max(times),
                    "min_time": min(times),
                    "total_time": sum(times)
                }
        
        return stats
    
    def get_connection_health(self) -> Dict[str, Any]:
        """Get connection pool health metrics."""
        if not self.connection_history:
            return {"status": "no_data", "message": "No connection metrics available"}
        
        latest = self.connection_history[-1]
        
        # Calculate health indicators
        utilization = (latest.checked_out / latest.pool_size) * 100 if latest.pool_size > 0 else 0
        overflow_ratio = (latest.overflow / latest.pool_size) * 100 if latest.pool_size > 0 else 0
        
        # Determine health status
        if utilization > 90:
            status = "critical"
        elif utilization > 75:
            status = "warning"
        elif overflow_ratio > 50:
            status = "warning"
        else:
            status = "healthy"
        
        return {
            "status": status,
            "utilization_percent": utilization,
            "overflow_ratio_percent": overflow_ratio,
            "pool_size": latest.pool_size,
            "checked_out": latest.checked_out,
            "checked_in": latest.checked_in,
            "overflow": latest.overflow,
            "invalid": latest.invalid,
            "timestamp": latest.timestamp.isoformat()
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get comprehensive performance report."""
        summary = self.get_query_performance_summary()
        connection_health = self.get_connection_health()
        slow_queries = self.get_slow_queries(5)
        query_stats = self.get_query_stats_by_statement()
        
        return {
            "timestamp": datetime.now(UTC).isoformat(),
            "query_performance": {
                "total_queries": summary.total_queries,
                "avg_execution_time": round(summary.avg_execution_time, 3),
                "max_execution_time": round(summary.max_execution_time, 3),
                "min_execution_time": round(summary.min_execution_time, 3),
                "error_rate_percent": round(summary.error_rate, 2),
                "slow_queries": summary.slow_queries,
                "slow_query_threshold": self.slow_query_threshold
            },
            "connection_health": connection_health,
            "slow_queries": [
                {
                    "query": q.query[:100] + "..." if len(q.query) > 100 else q.query,
                    "execution_time": round(q.execution_time, 3),
                    "timestamp": q.timestamp.isoformat(),
                    "error": q.error
                }
                for q in slow_queries
            ],
            "top_queries": dict(list(query_stats.items())[:10])  # Top 10 by count
        }
    
    def reset_metrics(self):
        """Reset all performance metrics."""
        self.query_history.clear()
        self.query_stats.clear()
        self.connection_history.clear()
        self.total_queries = 0
        self.total_errors = 0
        self.slow_queries = 0
        
        logger.info("Performance metrics reset")


# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def start_performance_monitoring(engine: Engine):
    """Start global performance monitoring."""
    monitor = get_performance_monitor()
    monitor.start_monitoring(engine)


def stop_performance_monitoring(engine: Engine):
    """Stop global performance monitoring."""
    monitor = get_performance_monitor()
    monitor.stop_monitoring(engine)
