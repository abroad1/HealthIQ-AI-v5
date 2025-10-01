"""
Profile repository for database operations.
"""

from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import logging

from core.models.database import Profile, ProfilePII, Consent, AuditLog, DeletionRequest
from repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ProfileRepository(BaseRepository[Profile]):
    """Repository for Profile entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(Profile, db_session)
    
    def get_by_user_id(self, user_id: UUID) -> Optional[Profile]:
        """
        Get profile by user ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Profile instance or None if not found
        """
        return self.get_by_field("user_id", user_id)
    
    def get_by_email(self, email: str) -> Optional[Profile]:
        """
        Get profile by email.
        
        Args:
            email: Email address
            
        Returns:
            Profile instance or None if not found
        """
        return self.get_by_field("email", email)
    
    def upsert_by_user_id(self, user_id: UUID, **kwargs) -> Profile:
        """
        Upsert profile by user ID.
        
        Args:
            user_id: User ID
            **kwargs: Fields to set/update
            
        Returns:
            Profile instance
        """
        return self.upsert({"user_id": user_id}, **kwargs)
    
    def update_consent(self, user_id: UUID, consent_given: bool, consent_version: str = "1.0") -> Optional[Profile]:
        """
        Update user consent information.
        
        Args:
            user_id: User ID
            consent_given: Whether consent was given
            consent_version: Consent version
            
        Returns:
            Updated profile instance or None if not found
        """
        try:
            from datetime import datetime
            update_data = {
                "consent_given": consent_given,
                "consent_version": consent_version,
                "consent_given_at": datetime.utcnow() if consent_given else None
            }
            return self.update_by_user_id(user_id, **update_data)
        except Exception as e:
            logger.error(f"Failed to update consent for user {user_id}: {str(e)}")
            raise
    
    def update_by_user_id(self, user_id: UUID, **kwargs) -> Optional[Profile]:
        """
        Update profile by user ID.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated profile instance or None if not found
        """
        try:
            profile = self.get_by_user_id(user_id)
            if not profile:
                return None
            
            for key, value in kwargs.items():
                if hasattr(profile, key):
                    setattr(profile, key, value)
            
            self.db_session.commit()
            self.db_session.refresh(profile)
            logger.info(f"Updated profile for user {user_id}")
            return profile
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to update profile for user {user_id}: {str(e)}")
            raise


class ProfilePIIRepository(BaseRepository[ProfilePII]):
    """Repository for ProfilePII entities (service-role only)."""
    
    def __init__(self, db_session: Session):
        super().__init__(ProfilePII, db_session)
    
    def get_by_profile_id(self, profile_id: UUID) -> Optional[ProfilePII]:
        """
        Get PII data by profile ID.
        
        Args:
            profile_id: Profile ID
            
        Returns:
            ProfilePII instance or None if not found
        """
        return self.get_by_field("profile_id", profile_id)
    
    def upsert_by_profile_id(self, profile_id: UUID, **kwargs) -> ProfilePII:
        """
        Upsert PII data by profile ID.
        
        Args:
            profile_id: Profile ID
            **kwargs: Fields to set/update
            
        Returns:
            ProfilePII instance
        """
        return self.upsert({"profile_id": profile_id}, **kwargs)


class ConsentRepository(BaseRepository[Consent]):
    """Repository for Consent entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(Consent, db_session)
    
    def list_by_user_id(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[Consent]:
        """
        List consents for a specific user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of consent instances
        """
        return self.list_by_field("user_id", user_id, limit, offset)
    
    def get_by_user_and_type(self, user_id: UUID, consent_type: str) -> Optional[Consent]:
        """
        Get consent by user ID and type.
        
        Args:
            user_id: User ID
            consent_type: Consent type
            
        Returns:
            Consent instance or None if not found
        """
        try:
            return (
                self.db_session.query(Consent)
                .filter(
                    and_(
                        Consent.user_id == user_id,
                        Consent.consent_type == consent_type
                    )
                )
                .first()
            )
        except Exception as e:
            logger.error(f"Failed to get consent for user {user_id}, type {consent_type}: {str(e)}")
            raise
    
    def upsert_by_user_and_type(self, user_id: UUID, consent_type: str, **kwargs) -> Consent:
        """
        Upsert consent by user ID and type.
        
        Args:
            user_id: User ID
            consent_type: Consent type
            **kwargs: Fields to set/update
            
        Returns:
            Consent instance
        """
        return self.upsert(
            {"user_id": user_id, "consent_type": consent_type},
            **kwargs
        )
    
    def revoke_consent(self, user_id: UUID, consent_type: str) -> Optional[Consent]:
        """
        Revoke consent for a user and type.
        
        Args:
            user_id: User ID
            consent_type: Consent type
            
        Returns:
            Updated consent instance or None if not found
        """
        try:
            from datetime import datetime
            consent = self.get_by_user_and_type(user_id, consent_type)
            if not consent:
                return None
            
            consent.granted = False
            consent.revoked_at = datetime.utcnow()
            self.db_session.commit()
            self.db_session.refresh(consent)
            logger.info(f"Revoked consent for user {user_id}, type {consent_type}")
            return consent
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to revoke consent for user {user_id}, type {consent_type}: {str(e)}")
            raise


class AuditLogRepository(BaseRepository[AuditLog]):
    """Repository for AuditLog entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(AuditLog, db_session)
    
    def list_by_user_id(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[AuditLog]:
        """
        List audit logs for a specific user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of audit log instances
        """
        return self.list_by_field("user_id", user_id, limit, offset)
    
    def list_by_action(self, action: str, limit: int = 100, offset: int = 0) -> List[AuditLog]:
        """
        List audit logs by action.
        
        Args:
            action: Action name
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of audit log instances
        """
        return self.list_by_field("action", action, limit, offset)
    
    def list_by_resource(self, resource_type: str, resource_id: UUID, limit: int = 100, offset: int = 0) -> List[AuditLog]:
        """
        List audit logs by resource.
        
        Args:
            resource_type: Resource type
            resource_id: Resource ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of audit log instances
        """
        try:
            return (
                self.db_session.query(AuditLog)
                .filter(
                    and_(
                        AuditLog.resource_type == resource_type,
                        AuditLog.resource_id == resource_id
                    )
                )
                .order_by(desc(AuditLog.created_at))
                .limit(limit)
                .offset(offset)
                .all()
            )
        except Exception as e:
            logger.error(f"Failed to list audit logs for resource {resource_type}:{resource_id}: {str(e)}")
            raise
    
    def log_action(self, action: str, resource_type: str, user_id: UUID = None, resource_id: UUID = None, 
                   details: Dict[str, Any] = None, ip_address: str = None, user_agent: str = None,
                   session_id: str = None, request_id: str = None, severity: str = "info", 
                   outcome: str = "success") -> AuditLog:
        """
        Log an action to the audit trail.
        
        Args:
            action: Action name
            resource_type: Resource type
            user_id: User ID (optional)
            resource_id: Resource ID (optional)
            details: Additional details (optional)
            ip_address: IP address (optional)
            user_agent: User agent (optional)
            session_id: Session ID (optional)
            request_id: Request ID (optional)
            severity: Severity level (optional)
            outcome: Outcome (optional)
            
        Returns:
            Created audit log instance
        """
        try:
            audit_log = AuditLog(
                action=action,
                resource_type=resource_type,
                user_id=user_id,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                user_agent=user_agent,
                session_id=session_id,
                request_id=request_id,
                severity=severity,
                outcome=outcome
            )
            self.db_session.add(audit_log)
            self.db_session.commit()
            self.db_session.refresh(audit_log)
            logger.info(f"Logged action {action} for resource {resource_type}")
            return audit_log
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to log action {action}: {str(e)}")
            raise


class DeletionRequestRepository(BaseRepository[DeletionRequest]):
    """Repository for DeletionRequest entities."""
    
    def __init__(self, db_session: Session):
        super().__init__(DeletionRequest, db_session)
    
    def list_by_user_id(self, user_id: UUID, limit: int = 100, offset: int = 0) -> List[DeletionRequest]:
        """
        List deletion requests for a specific user.
        
        Args:
            user_id: User ID
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of deletion request instances
        """
        return self.list_by_field("user_id", user_id, limit, offset)
    
    def list_by_status(self, status: str, limit: int = 100, offset: int = 0) -> List[DeletionRequest]:
        """
        List deletion requests by status.
        
        Args:
            status: Request status
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of deletion request instances
        """
        return self.list_by_field("status", status, limit, offset)
    
    def get_pending_requests(self, limit: int = 100, offset: int = 0) -> List[DeletionRequest]:
        """
        Get pending deletion requests.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of pending deletion request instances
        """
        return self.list_by_status("pending", limit, offset)
    
    def mark_completed(self, request_id: UUID) -> Optional[DeletionRequest]:
        """
        Mark deletion request as completed.
        
        Args:
            request_id: Request ID
            
        Returns:
            Updated deletion request instance or None if not found
        """
        try:
            from datetime import datetime
            return self.update(request_id, status="completed", completed_at=datetime.utcnow())
        except Exception as e:
            logger.error(f"Failed to mark deletion request as completed for {request_id}: {str(e)}")
            raise
    
    def mark_failed(self, request_id: UUID, error_message: str) -> Optional[DeletionRequest]:
        """
        Mark deletion request as failed.
        
        Args:
            request_id: Request ID
            error_message: Error message
            
        Returns:
            Updated deletion request instance or None if not found
        """
        try:
            return self.update(request_id, status="failed", error_message=error_message)
        except Exception as e:
            logger.error(f"Failed to mark deletion request as failed for {request_id}: {str(e)}")
            raise
