"""
Base repository class with common CRUD operations.
"""

from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, or_, desc, asc
import logging

from core.models.database import Base

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Base repository class with common CRUD operations."""
    
    def __init__(self, model: Type[T], db_session: Session):
        """
        Initialize the repository.
        
        Args:
            model: SQLAlchemy model class
            db_session: Database session
        """
        self.model = model
        self.db_session = db_session
    
    def create(self, **kwargs) -> T:
        """
        Create a new record.
        
        Args:
            **kwargs: Model attributes
            
        Returns:
            Created model instance
            
        Raises:
            SQLAlchemyError: If creation fails
        """
        try:
            instance = self.model(**kwargs)
            self.db_session.add(instance)
            self.db_session.commit()
            self.db_session.refresh(instance)
            logger.info(f"Created {self.model.__name__} with id: {instance.id}")
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Failed to create {self.model.__name__}: {str(e)}")
            raise
    
    def get_by_id(self, id: UUID) -> Optional[T]:
        """
        Get a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            Model instance or None if not found
        """
        try:
            return self.db_session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get {self.model.__name__} by id {id}: {str(e)}")
            raise
    
    def get_by_field(self, field_name: str, value: Any) -> Optional[T]:
        """
        Get a record by a specific field value.
        
        Args:
            field_name: Field name to filter by
            value: Field value
            
        Returns:
            Model instance or None if not found
        """
        try:
            field = getattr(self.model, field_name)
            return self.db_session.query(self.model).filter(field == value).first()
        except SQLAlchemyError as e:
            logger.error(f"Failed to get {self.model.__name__} by {field_name}={value}: {str(e)}")
            raise
    
    def list_by_field(self, field_name: str, value: Any, limit: int = 100, offset: int = 0) -> List[T]:
        """
        List records by a specific field value.
        
        Args:
            field_name: Field name to filter by
            value: Field value
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model instances
        """
        try:
            field = getattr(self.model, field_name)
            return (
                self.db_session.query(self.model)
                .filter(field == value)
                .order_by(desc(self.model.created_at))
                .limit(limit)
                .offset(offset)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Failed to list {self.model.__name__} by {field_name}={value}: {str(e)}")
            raise
    
    def list_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        """
        List all records.
        
        Args:
            limit: Maximum number of records to return
            offset: Number of records to skip
            
        Returns:
            List of model instances
        """
        try:
            return (
                self.db_session.query(self.model)
                .order_by(desc(self.model.created_at))
                .limit(limit)
                .offset(offset)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Failed to list all {self.model.__name__}: {str(e)}")
            raise
    
    def update(self, id: UUID, **kwargs) -> Optional[T]:
        """
        Update a record by ID.
        
        Args:
            id: Record ID
            **kwargs: Fields to update
            
        Returns:
            Updated model instance or None if not found
        """
        try:
            instance = self.get_by_id(id)
            if not instance:
                return None
            
            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)
            
            self.db_session.commit()
            self.db_session.refresh(instance)
            logger.info(f"Updated {self.model.__name__} with id: {id}")
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Failed to update {self.model.__name__} with id {id}: {str(e)}")
            raise
    
    def delete(self, id: UUID) -> bool:
        """
        Delete a record by ID.
        
        Args:
            id: Record ID
            
        Returns:
            True if deleted, False if not found
        """
        try:
            instance = self.get_by_id(id)
            if not instance:
                return False
            
            self.db_session.delete(instance)
            self.db_session.commit()
            logger.info(f"Deleted {self.model.__name__} with id: {id}")
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Failed to delete {self.model.__name__} with id {id}: {str(e)}")
            raise
    
    def upsert(self, filter_fields: Dict[str, Any], **kwargs) -> T:
        """
        Upsert a record (insert or update).
        
        Args:
            filter_fields: Fields to use for finding existing record
            **kwargs: Fields to set/update
            
        Returns:
            Model instance (created or updated)
        """
        try:
            # Try to find existing record
            query = self.db_session.query(self.model)
            for field_name, value in filter_fields.items():
                field = getattr(self.model, field_name)
                query = query.filter(field == value)
            
            instance = query.first()
            
            if instance:
                # Update existing record
                for key, value in kwargs.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)
                self.db_session.commit()
                self.db_session.refresh(instance)
                logger.info(f"Updated existing {self.model.__name__} with id: {instance.id}")
            else:
                # Create new record
                instance = self.model(**{**filter_fields, **kwargs})
                self.db_session.add(instance)
                self.db_session.commit()
                self.db_session.refresh(instance)
                logger.info(f"Created new {self.model.__name__} with id: {instance.id}")
            
            return instance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            logger.error(f"Failed to upsert {self.model.__name__}: {str(e)}")
            raise
    
    def count(self, **filters) -> int:
        """
        Count records with optional filters.
        
        Args:
            **filters: Field filters
            
        Returns:
            Number of records
        """
        try:
            query = self.db_session.query(self.model)
            for field_name, value in filters.items():
                field = getattr(self.model, field_name)
                query = query.filter(field == value)
            return query.count()
        except SQLAlchemyError as e:
            logger.error(f"Failed to count {self.model.__name__}: {str(e)}")
            raise
