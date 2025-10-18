"""
Connection Pooling Performance Tests

Tests database connection pooling performance, health checks, and load handling.
These tests validate that the connection pool can handle concurrent operations efficiently.
"""

import pytest
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy.orm import Session
from sqlalchemy import text

from config.database import get_engine, get_pool_status, test_connection
from services.monitoring.performance_monitor import get_performance_monitor


class TestConnectionPooling:
    """Test connection pooling performance and reliability."""
    
    def test_connection_pool_initialization(self):
        """Test that connection pool is properly initialized."""
        engine = get_engine()
        pool = engine.pool
        
        # Check pool configuration
        assert pool.size() > 0, "Pool size should be greater than 0"
        assert pool.checkedin() >= 0, "Checked in connections should be non-negative"
        assert pool.checkedout() >= 0, "Checked out connections should be non-negative"
        assert pool.overflow() >= 0, "Overflow connections should be non-negative"
    
    def test_connection_health_check(self):
        """Test database connection health check."""
        is_healthy = test_connection()
        assert is_healthy, "Database connection health check should pass"
    
    def test_pool_status_monitoring(self):
        """Test connection pool status monitoring."""
        status = get_pool_status()
        
        required_keys = ["pool_size", "checked_in", "checked_out", "overflow", "invalid"]
        for key in required_keys:
            assert key in status, f"Pool status should include {key}"
            assert isinstance(status[key], int), f"{key} should be an integer"
    
    def test_concurrent_connections(self, db_session: Session):
        """Test handling of concurrent database connections."""
        def execute_query(session_id: int):
            """Execute a simple query."""
            try:
                result = db_session.execute(text("SELECT :session_id as id, NOW() as timestamp"), 
                                          {"session_id": session_id})
                return result.fetchone()
            except Exception as e:
                return {"error": str(e), "session_id": session_id}
        
        # Test with multiple concurrent connections
        num_threads = 10
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(execute_query, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]
        
        # Verify all queries executed successfully
        successful_results = [r for r in results if "error" not in r]
        assert len(successful_results) == num_threads, "All concurrent queries should succeed"
    
    def test_connection_pool_exhaustion(self, db_session: Session):
        """Test behavior when connection pool is exhausted."""
        # This test simulates high load to test pool overflow behavior
        def long_running_query(session_id: int):
            """Execute a long-running query."""
            try:
                # Simulate a longer operation
                result = db_session.execute(text("SELECT pg_sleep(0.1), :session_id as id"), 
                                          {"session_id": session_id})
                return result.fetchone()
            except Exception as e:
                return {"error": str(e), "session_id": session_id}
        
        # Test with more threads than pool size
        num_threads = 25  # More than typical pool size
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(long_running_query, i) for i in range(num_threads)]
            results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify pool handled overflow gracefully
        successful_results = [r for r in results if "error" not in r]
        assert len(successful_results) == num_threads, "Pool should handle overflow gracefully"
        
        # Verify reasonable execution time (should not be too slow due to queuing)
        assert execution_time < 10.0, f"Execution time {execution_time:.2f}s should be reasonable"
    
    def test_connection_reuse(self, db_session: Session):
        """Test that connections are properly reused."""
        initial_pool_status = get_pool_status()
        
        # Execute multiple queries
        for i in range(5):
            result = db_session.execute(text("SELECT :i as iteration"), {"i": i})
            assert result.fetchone()[0] == i
        
        final_pool_status = get_pool_status()
        
        # Pool should not have grown significantly
        assert final_pool_status["pool_size"] == initial_pool_status["pool_size"]
        assert final_pool_status["checked_out"] <= initial_pool_status["pool_size"]
    
    def test_connection_cleanup(self, db_session: Session):
        """Test that connections are properly cleaned up."""
        initial_status = get_pool_status()
        
        # Execute queries and ensure cleanup
        for i in range(3):
            with db_session.begin():
                result = db_session.execute(text("SELECT :i as iteration"), {"i": i})
                assert result.fetchone()[0] == i
        
        # Force garbage collection
        import gc
        gc.collect()
        
        final_status = get_pool_status()
        
        # Checked out connections should be minimal after cleanup
        assert final_status["checked_out"] <= 1, "Most connections should be returned to pool"
    
    def test_performance_monitoring_integration(self, db_session: Session):
        """Test that performance monitoring works with connection pooling."""
        monitor = get_performance_monitor()
        
        # Execute some queries
        for i in range(3):
            db_session.execute(text("SELECT :i as iteration"), {"i": i})
        
        # Get performance summary
        summary = monitor.get_query_performance_summary()
        
        assert summary.total_queries >= 3, "Should have recorded at least 3 queries"
        assert summary.avg_execution_time >= 0, "Average execution time should be non-negative"
        assert summary.max_execution_time >= 0, "Max execution time should be non-negative"
    
    def test_slow_query_detection(self, db_session: Session):
        """Test slow query detection and logging."""
        monitor = get_performance_monitor()
        
        # Execute a slow query (simulated)
        start_time = time.time()
        db_session.execute(text("SELECT pg_sleep(0.5)"))  # 500ms sleep
        execution_time = time.time() - start_time
        
        # Check if slow query was detected
        slow_queries = monitor.get_slow_queries()
        
        # Should have at least one slow query if threshold is < 0.5s
        if monitor.slow_query_threshold < 0.5:
            assert len(slow_queries) >= 1, "Slow query should be detected"
    
    def test_connection_pool_metrics(self, db_session: Session):
        """Test connection pool metrics collection."""
        monitor = get_performance_monitor()
        
        # Record connection metrics
        pool_status = get_pool_status()
        monitor.record_connection_metrics(pool_status)
        
        # Get connection health
        health = monitor.get_connection_health()
        
        assert "status" in health, "Health status should be available"
        assert "utilization_percent" in health, "Utilization should be tracked"
        assert "pool_size" in health, "Pool size should be tracked"
        assert health["pool_size"] > 0, "Pool size should be positive"
    
    def test_high_load_performance(self, db_session: Session):
        """Test performance under high load."""
        monitor = get_performance_monitor()
        
        def execute_workload(thread_id: int, num_queries: int):
            """Execute a workload of queries."""
            results = []
            for i in range(num_queries):
                try:
                    result = db_session.execute(
                        text("SELECT :thread_id as thread, :query_id as query, NOW() as timestamp"),
                        {"thread_id": thread_id, "query_id": i}
                    )
                    results.append(result.fetchone())
                except Exception as e:
                    results.append({"error": str(e), "thread_id": thread_id, "query_id": i})
            return results
        
        # High load test
        num_threads = 8
        queries_per_thread = 10
        total_queries = num_threads * queries_per_thread
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(execute_workload, i, queries_per_thread) 
                for i in range(num_threads)
            ]
            all_results = [future.result() for future in as_completed(futures)]
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Verify all queries completed
        successful_queries = sum(
            len([r for r in thread_results if "error" not in r]) 
            for thread_results in all_results
        )
        
        assert successful_queries == total_queries, f"All {total_queries} queries should succeed"
        
        # Verify reasonable performance
        queries_per_second = total_queries / total_time
        assert queries_per_second > 10, f"Should handle at least 10 queries/second, got {queries_per_second:.2f}"
        
        # Verify performance monitoring captured the load
        summary = monitor.get_query_performance_summary()
        assert summary.total_queries >= total_queries, "Performance monitor should track all queries"
