"""
GDPR Compliance Tests

Tests GDPR compliance features including consent tracking, data deletion,
audit logging, and user data portability.
"""

import pytest
from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy.orm import Session

from core.models.database import (
    Profile, ProfilePII, Consent, AuditLog, DeletionRequest, Analysis
)


class TestGDPRCompliance:
    """Test GDPR compliance features."""
    
    def test_consent_tracking_creation(self, db_session: Session):
        """Test that consent records are properly created."""
        user_id = uuid4()
        
        # Create profile with consent
        profile = Profile(
            user_id=user_id,
            email="test@example.com",
            consent_given=True,
            consent_version="1.0",
            consent_given_at=datetime.now(UTC)
        )
        db_session.add(profile)
        db_session.commit()
        
        # Create explicit consent record
        consent = Consent(
            user_id=user_id,
            consent_type="data_processing",
            granted=True,
            granted_at=datetime.now(UTC),
            version="1.0",
            consent_text="I consent to data processing",
            legal_basis="consent"
        )
        db_session.add(consent)
        db_session.commit()
        
        # Verify consent record exists
        saved_consent = db_session.query(Consent).filter_by(user_id=user_id).first()
        assert saved_consent is not None
        assert saved_consent.granted is True
        assert saved_consent.consent_type == "data_processing"
        assert saved_consent.legal_basis == "consent"
    
    def test_consent_withdrawal(self, db_session: Session):
        """Test consent withdrawal functionality."""
        user_id = uuid4()
        
        # Create initial consent
        consent = Consent(
            user_id=user_id,
            consent_type="data_processing",
            granted=True,
            granted_at=datetime.now(UTC),
            version="1.0"
        )
        db_session.add(consent)
        db_session.commit()
        
        # Withdraw consent
        consent.granted = False
        consent.revoked_at = datetime.now(UTC)
        db_session.commit()
        
        # Verify consent withdrawal
        updated_consent = db_session.query(Consent).filter_by(user_id=user_id).first()
        assert updated_consent.granted is False
        assert updated_consent.revoked_at is not None
    
    def test_audit_logging(self, db_session: Session):
        """Test comprehensive audit logging."""
        user_id = uuid4()
        
        # Create audit log entry
        audit_log = AuditLog(
            user_id=user_id,
            action="data_access",
            resource_type="profile",
            resource_id=uuid4(),
            details={"field": "email", "operation": "read"},
            ip_address="192.168.1.1",
            user_agent="Test Browser",
            session_id="test_session_123",
            request_id="req_456",
            severity="info",
            outcome="success"
        )
        db_session.add(audit_log)
        db_session.commit()
        
        # Verify audit log
        saved_log = db_session.query(AuditLog).filter_by(user_id=user_id).first()
        assert saved_log is not None
        assert saved_log.action == "data_access"
        assert saved_log.details["field"] == "email"
        assert saved_log.outcome == "success"
    
    def test_deletion_request_creation(self, db_session: Session):
        """Test GDPR deletion request creation."""
        user_id = uuid4()
        
        # Create deletion request
        deletion_request = DeletionRequest(
            user_id=user_id,
            status="pending",
            request_type="full_deletion",
            reason="User requested data deletion",
            verification_method="email",
            verification_completed=False
        )
        db_session.add(deletion_request)
        db_session.commit()
        
        # Verify deletion request
        saved_request = db_session.query(DeletionRequest).filter_by(user_id=user_id).first()
        assert saved_request is not None
        assert saved_request.status == "pending"
        assert saved_request.request_type == "full_deletion"
        assert saved_request.verification_completed is False
    
    def test_deletion_request_processing(self, db_session: Session):
        """Test deletion request processing workflow."""
        user_id = uuid4()
        
        # Create deletion request
        deletion_request = DeletionRequest(
            user_id=user_id,
            status="pending",
            request_type="full_deletion"
        )
        db_session.add(deletion_request)
        db_session.commit()
        
        # Process deletion request
        deletion_request.status = "processing"
        deletion_request.verification_completed = True
        db_session.commit()
        
        # Complete deletion request
        deletion_request.status = "completed"
        deletion_request.completed_at = datetime.now(UTC)
        db_session.commit()
        
        # Verify processing
        updated_request = db_session.query(DeletionRequest).filter_by(user_id=user_id).first()
        assert updated_request.status == "completed"
        assert updated_request.verification_completed is True
        assert updated_request.completed_at is not None
    
    def test_pii_data_isolation(self, db_session: Session):
        """Test that PII data is properly isolated."""
        user_id = uuid4()
        
        # Create profile
        profile = Profile(
            user_id=user_id,
            email="test@example.com",
            consent_given=True
        )
        db_session.add(profile)
        db_session.commit()
        
        # Create PII data (service role only)
        pii_data = ProfilePII(
            profile_id=profile.id,
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime(1990, 1, 1),
            phone_number="+1234567890",
            address={"street": "123 Main St", "city": "Anytown"}
        )
        db_session.add(pii_data)
        db_session.commit()
        
        # Verify PII data exists
        saved_pii = db_session.query(ProfilePII).filter_by(profile_id=profile.id).first()
        assert saved_pii is not None
        assert saved_pii.first_name == "John"
        assert saved_pii.last_name == "Doe"
    
    def test_data_portability_export(self, db_session: Session):
        """Test data portability through export functionality."""
        user_id = uuid4()
        
        # Create user data
        profile = Profile(
            user_id=user_id,
            email="test@example.com",
            consent_given=True
        )
        db_session.add(profile)
        db_session.commit()
        
        # Create analysis data
        analysis = Analysis(
            user_id=user_id,
            status="completed",
            analysis_version="1.0.0"
        )
        db_session.add(analysis)
        db_session.commit()
        
        # Verify data exists for export
        user_profile = db_session.query(Profile).filter_by(user_id=user_id).first()
        user_analyses = db_session.query(Analysis).filter_by(user_id=user_id).all()
        
        assert user_profile is not None
        assert len(user_analyses) == 1
        assert user_analyses[0].user_id == user_id
    
    def test_consent_version_tracking(self, db_session: Session):
        """Test consent version tracking for compliance."""
        user_id = uuid4()
        
        # Create consent with version 1.0
        consent_v1 = Consent(
            user_id=user_id,
            consent_type="data_processing",
            granted=True,
            version="1.0",
            granted_at=datetime.now(UTC)
        )
        db_session.add(consent_v1)
        db_session.commit()
        
        # Update consent to version 2.0
        consent_v2 = Consent(
            user_id=user_id,
            consent_type="data_processing",
            granted=True,
            version="2.0",
            granted_at=datetime.now(UTC)
        )
        db_session.add(consent_v2)
        db_session.commit()
        
        # Verify both versions exist
        consents = db_session.query(Consent).filter_by(user_id=user_id).all()
        assert len(consents) == 2
        
        versions = [c.version for c in consents]
        assert "1.0" in versions
        assert "2.0" in versions
    
    def test_legal_basis_tracking(self, db_session: Session):
        """Test legal basis tracking for GDPR compliance."""
        user_id = uuid4()
        
        # Create consent with different legal bases
        legal_bases = ["consent", "legitimate_interest", "contract", "legal_obligation"]
        
        for i, basis in enumerate(legal_bases):
            consent = Consent(
                user_id=user_id,
                consent_type="data_processing",
                granted=True,
                legal_basis=basis,
                granted_at=datetime.now(UTC)
            )
            db_session.add(consent)
        
        db_session.commit()
        
        # Verify all legal bases are tracked
        consents = db_session.query(Consent).filter_by(user_id=user_id).all()
        assert len(consents) == len(legal_bases)
        
        tracked_bases = [c.legal_basis for c in consents]
        for basis in legal_bases:
            assert basis in tracked_bases
    
    def test_audit_trail_completeness(self, db_session: Session):
        """Test that audit trail captures all required information."""
        user_id = uuid4()
        
        # Create comprehensive audit log
        audit_log = AuditLog(
            user_id=user_id,
            action="data_export",
            resource_type="profile",
            resource_id=uuid4(),
            details={
                "export_type": "json",
                "data_categories": ["profile", "analyses"],
                "export_size": 1024
            },
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Test Browser)",
            session_id="session_789",
            request_id="req_123",
            severity="info",
            outcome="success"
        )
        db_session.add(audit_log)
        db_session.commit()
        
        # Verify audit trail completeness
        saved_log = db_session.query(AuditLog).filter_by(user_id=user_id).first()
        
        # Required fields
        assert saved_log.user_id == user_id
        assert saved_log.action is not None
        assert saved_log.resource_type is not None
        assert saved_log.created_at is not None
        
        # Optional but important fields
        assert saved_log.details is not None
        assert saved_log.ip_address is not None
        assert saved_log.user_agent is not None
        assert saved_log.session_id is not None
        assert saved_log.request_id is not None
        assert saved_log.severity is not None
        assert saved_log.outcome is not None
    
    def test_data_minimization_principle(self, db_session: Session):
        """Test that only necessary data is collected."""
        user_id = uuid4()
        
        # Create profile with minimal necessary data
        profile = Profile(
            user_id=user_id,
            email="test@example.com",  # Necessary for authentication
            consent_given=True,        # Necessary for GDPR compliance
            consent_version="1.0"      # Necessary for compliance tracking
        )
        db_session.add(profile)
        db_session.commit()
        
        # Verify only necessary fields are populated
        saved_profile = db_session.query(Profile).filter_by(user_id=user_id).first()
        assert saved_profile.email is not None
        assert saved_profile.consent_given is not None
        assert saved_profile.consent_version is not None
        
        # Optional fields should be None (data minimization)
        assert saved_profile.demographics is None
        assert saved_profile.consent_given_at is None
    
    def test_right_to_erasure_implementation(self, db_session: Session):
        """Test implementation of right to erasure (right to be forgotten)."""
        user_id = uuid4()
        
        # Create user data
        profile = Profile(
            user_id=user_id,
            email="test@example.com",
            consent_given=True
        )
        db_session.add(profile)
        db_session.commit()
        
        # Create deletion request
        deletion_request = DeletionRequest(
            user_id=user_id,
            status="pending",
            request_type="full_deletion"
        )
        db_session.add(deletion_request)
        db_session.commit()
        
        # Simulate data deletion (in real implementation, this would cascade)
        db_session.delete(profile)
        db_session.commit()
        
        # Verify data is deleted
        deleted_profile = db_session.query(Profile).filter_by(user_id=user_id).first()
        assert deleted_profile is None
        
        # Deletion request should remain for audit purposes
        deletion_record = db_session.query(DeletionRequest).filter_by(user_id=user_id).first()
        assert deletion_record is not None
