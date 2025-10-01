"""
SQLAlchemy database models for HealthIQ AI v5.
Full schema with proper fields, relationships, constraints, and indexes.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import uuid4

from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, 
    ForeignKey, JSON, ARRAY, Enum as SQLEnum, Index, CheckConstraint,
    UniqueConstraint, func
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

# SQLAlchemy Base
Base = declarative_base()


class Profile(Base):
    """User profile model."""
    __tablename__ = "profiles"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key to auth.users
    user_id = Column(UUID(as_uuid=True), nullable=False, unique=True, index=True)
    
    # Basic profile data
    email = Column(String(255), nullable=False, unique=True, index=True)
    demographics = Column(JSON, nullable=True)
    
    # GDPR compliance fields
    consent_given = Column(Boolean, nullable=False, default=False)
    consent_version = Column(String(20), nullable=False, default="1.0")
    consent_given_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="profile", cascade="all, delete-orphan")
    exports = relationship("Export", back_populates="profile", cascade="all, delete-orphan")
    consents = relationship("Consent", back_populates="profile", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="profile", cascade="all, delete-orphan")
    deletion_requests = relationship("DeletionRequest", back_populates="profile", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("email ~ '^[^@]+@[^@]+\\.[^@]+$'", name="ck_profiles_email_format"),
        CheckConstraint("consent_version ~ '^\\d+\\.\\d+$'", name="ck_profiles_consent_version_format"),
        Index("idx_profiles_user_id_created_at", "user_id", "created_at"),
        Index("idx_profiles_consent_given", "consent_given"),
    )


class ProfilePII(Base):
    """User PII model (service-role only access)."""
    __tablename__ = "profiles_pii"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key to profiles
    profile_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id"), nullable=False, unique=True)
    
    # PII data (encrypted in production)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    phone_number = Column(String(20), nullable=True)
    address = Column(JSON, nullable=True)  # Structured address data
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    profile = relationship("Profile", backref="pii_data")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("phone_number ~ '^\\+?[1-9]\\d{1,14}$'", name="ck_profiles_pii_phone_format"),
        Index("idx_profiles_pii_profile_id", "profile_id"),
    )


class Analysis(Base):
    """Analysis session model."""
    __tablename__ = "analyses"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=False, index=True)
    
    # Analysis data
    status = Column(SQLEnum("pending", "processing", "completed", "failed", name="analysis_status"), 
                   nullable=False, default="pending", index=True)
    raw_biomarkers = Column(JSON, nullable=True)
    questionnaire_data = Column(JSON, nullable=True)
    
    # Performance tracking
    processing_time_seconds = Column(Float, nullable=True)
    
    # Metadata
    analysis_version = Column(String(20), nullable=False, default="1.0.0")
    pipeline_version = Column(String(20), nullable=False, default="1.0.0")
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    completed_at = Column(DateTime, nullable=True, index=True)
    
    # Relationships
    profile = relationship("Profile", back_populates="analyses")
    result = relationship("AnalysisResult", back_populates="analysis", uselist=False, cascade="all, delete-orphan")
    biomarker_scores = relationship("BiomarkerScore", back_populates="analysis", cascade="all, delete-orphan")
    clusters = relationship("Cluster", back_populates="analysis", cascade="all, delete-orphan")
    insights = relationship("Insight", back_populates="analysis", cascade="all, delete-orphan")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("processing_time_seconds >= 0", name="ck_analyses_processing_time_positive"),
        CheckConstraint("analysis_version ~ '^\\d+\\.\\d+\\.\\d+$'", name="ck_analyses_version_format"),
        CheckConstraint("pipeline_version ~ '^\\d+\\.\\d+\\.\\d+$'", name="ck_analyses_pipeline_version_format"),
        Index("idx_analyses_user_id_created_at", "user_id", "created_at"),
        Index("idx_analyses_user_id_status", "user_id", "status"),
        Index("idx_analyses_completed_at", "completed_at"),
        Index("idx_analyses_analysis_version", "analysis_version"),
    )


class AnalysisResult(Base):
    """Analysis results model."""
    __tablename__ = "analysis_results"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign key
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), 
                        nullable=False, unique=True, index=True)
    
    # Result data
    biomarkers = Column(JSON, nullable=True)
    clusters = Column(JSON, nullable=True)
    insights = Column(JSON, nullable=True)
    overall_score = Column(Float, nullable=True)
    risk_assessment = Column(JSON, nullable=True)
    recommendations = Column(ARRAY(Text), nullable=True)
    
    # Metadata
    result_version = Column(String(50), nullable=False, default="1.0.0", index=True)
    confidence_score = Column(Float, nullable=True)
    processing_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="result")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("overall_score >= 0 AND overall_score <= 1", name="ck_analysis_results_score_range"),
        CheckConstraint("confidence_score >= 0 AND confidence_score <= 1", name="ck_analysis_results_confidence_range"),
        CheckConstraint("result_version ~ '^\\d+\\.\\d+\\.\\d+$'", name="ck_analysis_results_version_format"),
        Index("idx_analysis_results_analysis_id", "analysis_id"),
        Index("idx_analysis_results_overall_score", "overall_score"),
        Index("idx_analysis_results_created_at", "created_at"),
    )


class BiomarkerScore(Base):
    """Individual biomarker scores model."""
    __tablename__ = "biomarker_scores"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False, index=True)
    
    # Biomarker data
    biomarker_name = Column(String(100), nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=True)
    score = Column(Float, nullable=True)
    percentile = Column(Float, nullable=True)
    status = Column(String(20), nullable=True, index=True)
    reference_range = Column(JSON, nullable=True)
    interpretation = Column(Text, nullable=True)
    
    # Additional metadata
    confidence = Column(Float, nullable=True)
    health_system = Column(String(50), nullable=True, index=True)
    critical_flag = Column(Boolean, nullable=False, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="biomarker_scores")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("value >= 0", name="ck_biomarker_scores_value_positive"),
        CheckConstraint("score >= 0 AND score <= 1", name="ck_biomarker_scores_score_range"),
        CheckConstraint("percentile >= 0 AND percentile <= 100", name="ck_biomarker_scores_percentile_range"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_biomarker_scores_confidence_range"),
        CheckConstraint("status IN ('optimal', 'normal', 'elevated', 'low', 'critical')", name="ck_biomarker_scores_status_valid"),
        Index("idx_biomarker_scores_analysis_id", "analysis_id"),
        Index("idx_biomarker_scores_biomarker_name", "biomarker_name"),
        Index("idx_biomarker_scores_analysis_biomarker", "analysis_id", "biomarker_name"),
        Index("idx_biomarker_scores_status", "status"),
        Index("idx_biomarker_scores_health_system", "health_system"),
        Index("idx_biomarker_scores_critical_flag", "critical_flag"),
    )


class Cluster(Base):
    """Health cluster data model."""
    __tablename__ = "clusters"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False, index=True)
    
    # Cluster data
    cluster_name = Column(String(100), nullable=False, index=True)
    cluster_type = Column(String(50), nullable=False, index=True)
    score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    biomarkers = Column(ARRAY(String), nullable=True)
    insights = Column(JSON, nullable=True)
    
    # Additional metadata
    severity = Column(String(20), nullable=True, index=True)
    description = Column(Text, nullable=True)
    health_system = Column(String(50), nullable=True, index=True)
    algorithm_used = Column(String(50), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="clusters")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("score >= 0 AND score <= 1", name="ck_clusters_score_range"),
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_clusters_confidence_range"),
        CheckConstraint("severity IN ('normal', 'mild', 'moderate', 'high', 'critical')", name="ck_clusters_severity_valid"),
        Index("idx_clusters_analysis_id", "analysis_id"),
        Index("idx_clusters_cluster_type", "cluster_type"),
        Index("idx_clusters_analysis_type", "analysis_id", "cluster_type"),
        Index("idx_clusters_severity", "severity"),
        Index("idx_clusters_health_system", "health_system"),
    )


class Insight(Base):
    """Individual insight model."""
    __tablename__ = "insights"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=False, index=True)
    
    # Insight data
    insight_type = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=True, index=True)  # Made nullable for Sprint 9c
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    confidence = Column(Float, nullable=True)
    priority = Column(String(20), nullable=True, index=True)
    actionable = Column(Boolean, default=True, nullable=False)
    
    # Provenance fields (Sprint 9c)
    insight_id = Column(String(100), nullable=False, index=True)
    version = Column(String(20), nullable=False, index=True)
    manifest_id = Column(String(100), nullable=False, index=True)
    experiment_id = Column(String(100), nullable=True)
    drivers = Column(JSON, nullable=True)
    evidence = Column(JSON, nullable=True)
    error_code = Column(String(50), nullable=True)
    error_detail = Column(Text, nullable=True)
    latency_ms = Column(Integer, nullable=False, default=0)
    
    # Additional metadata
    severity = Column(String(20), nullable=True, index=True)
    biomarkers_involved = Column(ARRAY(String), nullable=True)
    health_system = Column(String(50), nullable=True, index=True)
    recommendations = Column(ARRAY(Text), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False)
    
    # Relationships
    analysis = relationship("Analysis", back_populates="insights")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="ck_insights_confidence_range"),
        CheckConstraint("priority IN ('low', 'medium', 'high', 'critical')", name="ck_insights_priority_valid"),
        CheckConstraint("severity IN ('normal', 'mild', 'moderate', 'high', 'critical')", name="ck_insights_severity_valid"),
        CheckConstraint("latency_ms >= 0", name="ck_insights_latency_positive"),
        Index("idx_insights_analysis_id", "analysis_id"),
        Index("idx_insights_category", "category"),
        Index("idx_insights_analysis_category", "analysis_id", "category"),
        Index("idx_insights_priority", "priority"),
        Index("idx_insights_severity", "severity"),
        Index("idx_insights_health_system", "health_system"),
        Index("idx_insights_actionable", "actionable"),
        # New provenance indexes
        Index("idx_insights_insight_id_version", "insight_id", "version"),
        Index("idx_insights_manifest_id", "manifest_id"),
        Index("idx_insights_drivers_gin", "drivers", postgresql_using="gin"),
        Index("idx_insights_evidence_gin", "evidence", postgresql_using="gin"),
        # Unique constraint for analysis + insight + version
        UniqueConstraint("analysis_id", "insight_id", "version", name="idx_insights_unique_analysis_insight_version"),
    )


class Export(Base):
    """Export requests and results model."""
    __tablename__ = "exports"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=False, index=True)
    analysis_id = Column(UUID(as_uuid=True), ForeignKey("analyses.id"), nullable=True, index=True)
    
    # Export data
    export_type = Column(SQLEnum("pdf", "json", "csv", name="export_type"), nullable=False, index=True)
    status = Column(SQLEnum("pending", "processing", "completed", "failed", name="export_status"), 
                   nullable=False, default="pending", index=True)
    file_path = Column(String(500), nullable=True)
    file_size_bytes = Column(Integer, nullable=True)
    
    # Additional metadata
    download_url = Column(String(1000), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    processing_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True, index=True)
    
    # Relationships
    profile = relationship("Profile", back_populates="exports")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("file_size_bytes >= 0", name="ck_exports_file_size_positive"),
        Index("idx_exports_user_id", "user_id"),
        Index("idx_exports_status", "status"),
        Index("idx_exports_user_id_status", "user_id", "status"),
        Index("idx_exports_analysis_id", "analysis_id"),
        Index("idx_exports_export_type", "export_type"),
        Index("idx_exports_created_at", "created_at"),
        Index("idx_exports_expires_at", "expires_at"),
    )


class Consent(Base):
    """User consent and privacy preferences model."""
    __tablename__ = "consents"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=False, index=True)
    
    # Consent data
    consent_type = Column(String(50), nullable=False, index=True)
    granted = Column(Boolean, nullable=False, default=False, index=True)
    granted_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)
    version = Column(String(20), nullable=False, default="1.0")
    
    # Additional metadata
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    consent_text = Column(Text, nullable=True)
    legal_basis = Column(String(100), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    profile = relationship("Profile", back_populates="consents")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("version ~ '^\\d+\\.\\d+$'", name="ck_consents_version_format"),
        CheckConstraint("consent_type IN ('data_processing', 'marketing', 'analytics', 'third_party')", name="ck_consents_type_valid"),
        CheckConstraint("legal_basis IN ('consent', 'legitimate_interest', 'contract', 'legal_obligation')", name="ck_consents_legal_basis_valid"),
        Index("idx_consents_user_id", "user_id"),
        Index("idx_consents_type", "consent_type"),
        Index("idx_consents_user_id_type", "user_id", "consent_type"),
        Index("idx_consents_granted", "granted"),
        Index("idx_consents_created_at", "created_at"),
    )


class AuditLog(Base):
    """Audit trail for compliance and debugging."""
    __tablename__ = "audit_logs"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=True, index=True)
    
    # Audit data
    action = Column(String(100), nullable=False, index=True)
    resource_type = Column(String(50), nullable=False, index=True)
    resource_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Additional metadata
    session_id = Column(String(100), nullable=True, index=True)
    request_id = Column(String(100), nullable=True, index=True)
    severity = Column(String(20), nullable=True, index=True)
    outcome = Column(String(20), nullable=True, index=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    
    # Relationships
    profile = relationship("Profile", back_populates="audit_logs")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("severity IN ('info', 'warning', 'error', 'critical')", name="ck_audit_logs_severity_valid"),
        CheckConstraint("outcome IN ('success', 'failure', 'partial')", name="ck_audit_logs_outcome_valid"),
        Index("idx_audit_logs_user_id", "user_id"),
        Index("idx_audit_logs_action", "action"),
        Index("idx_audit_logs_created_at", "created_at"),
        Index("idx_audit_logs_user_id_created_at", "user_id", "created_at"),
        Index("idx_audit_logs_resource_type", "resource_type"),
        Index("idx_audit_logs_session_id", "session_id"),
        Index("idx_audit_logs_severity", "severity"),
        Index("idx_audit_logs_outcome", "outcome"),
    )


class DeletionRequest(Base):
    """GDPR deletion requests model."""
    __tablename__ = "deletion_requests"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Foreign keys
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.user_id"), nullable=False, index=True)
    
    # Deletion data
    status = Column(SQLEnum("pending", "processing", "completed", "failed", name="deletion_status"), 
                   nullable=False, default="pending", index=True)
    reason = Column(Text, nullable=True)
    requested_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    completed_at = Column(DateTime, nullable=True, index=True)
    
    # Additional metadata
    request_type = Column(String(50), nullable=False, default="full_deletion", index=True)
    verification_method = Column(String(50), nullable=True)
    verification_completed = Column(Boolean, nullable=False, default=False)
    error_message = Column(Text, nullable=True)
    processing_metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    profile = relationship("Profile", back_populates="deletion_requests")
    
    # Constraints and indexes
    __table_args__ = (
        CheckConstraint("request_type IN ('full_deletion', 'data_export', 'consent_withdrawal')", name="ck_deletion_requests_type_valid"),
        CheckConstraint("verification_method IN ('email', 'phone', 'id_document', 'manual_review')", name="ck_deletion_requests_verification_valid"),
        Index("idx_deletion_requests_user_id", "user_id"),
        Index("idx_deletion_requests_status", "status"),
        Index("idx_deletion_requests_user_id_status", "user_id", "status"),
        Index("idx_deletion_requests_requested_at", "requested_at"),
        Index("idx_deletion_requests_completed_at", "completed_at"),
        Index("idx_deletion_requests_request_type", "request_type"),
    )
