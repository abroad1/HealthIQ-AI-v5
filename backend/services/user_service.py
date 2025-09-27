"""
User service - handles user-related operations.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
from core.models.user import User, UserContext


class UserService:
    """Service for handling user-related operations."""
    
    def __init__(self):
        """Initialize the user service."""
        # In-memory storage for demo purposes - replace with database in production
        self._users: Dict[str, User] = {}
        self._user_contexts: Dict[str, UserContext] = {}
    
    async def create_user(self, user_data: Dict[str, Any]) -> User:
        """
        Create a new user.
        
        Args:
            user_data: User information dictionary
            
        Returns:
            Created User object
        """
        # Generate user ID if not provided
        user_id = user_data.get("user_id", str(uuid.uuid4()))
        
        # Create user object
        user = User(
            user_id=user_id,
            email=user_data.get("email"),
            age=user_data.get("age"),
            gender=user_data.get("gender"),
            height=user_data.get("height"),
            weight=user_data.get("weight"),
            ethnicity=user_data.get("ethnicity"),
            medical_history=user_data.get("medical_history", {}),
            medications=user_data.get("medications", []),
            lifestyle_factors=user_data.get("lifestyle_factors", {}),
            created_at=datetime.now(timezone.utc).isoformat(),
            updated_at=datetime.now(timezone.utc).isoformat()
        )
        
        # Store user
        self._users[user_id] = user
        
        return user
    
    async def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            user_id: User identifier
            
        Returns:
            User object or None if not found
        """
        return self._users.get(user_id)
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Optional[User]:
        """
        Update user information.
        
        Args:
            user_id: User identifier
            update_data: Dictionary with fields to update
            
        Returns:
            Updated User object or None if not found
        """
        user = self._users.get(user_id)
        if not user:
            return None
        
        # Create updated user data
        updated_data = user.model_dump()
        updated_data.update(update_data)
        updated_data["updated_at"] = datetime.now(timezone.utc).isoformat()
        
        # Create new user object (immutable)
        updated_user = User(**updated_data)
        
        # Store updated user
        self._users[user_id] = updated_user
        
        return updated_user
    
    async def delete_user(self, user_id: str) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if deleted, False if not found
        """
        if user_id in self._users:
            del self._users[user_id]
            # Also remove user context if exists
            if user_id in self._user_contexts:
                del self._user_contexts[user_id]
            return True
        return False
    
    async def list_users(self, limit: int = 100, offset: int = 0) -> List[User]:
        """
        List users with pagination.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            
        Returns:
            List of User objects
        """
        user_list = list(self._users.values())
        
        # Sort by creation date (newest first)
        user_list.sort(key=lambda x: x.created_at or "", reverse=True)
        
        # Apply pagination
        return user_list[offset:offset + limit]
    
    async def validate_user_data(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate user data before creation or update.
        
        Args:
            user_data: User data to validate
            
        Returns:
            Validation results dictionary
        """
        errors = []
        warnings = []
        
        # Validate email format
        email = user_data.get("email")
        if email and "@" not in email:
            errors.append("Invalid email format")
        
        # Validate age
        age = user_data.get("age")
        if age is not None:
            if not isinstance(age, int) or age < 0 or age > 150:
                errors.append("Age must be a valid integer between 0 and 150")
        
        # Validate gender
        gender = user_data.get("gender")
        if gender and gender.lower() not in ["male", "female", "other", "prefer_not_to_say"]:
            warnings.append("Gender value not in standard options")
        
        # Validate height and weight
        height = user_data.get("height")
        if height is not None and (not isinstance(height, (int, float)) or height <= 0 or height > 300):
            errors.append("Height must be a positive number between 0 and 300 cm")
        
        weight = user_data.get("weight")
        if weight is not None and (not isinstance(weight, (int, float)) or weight <= 0 or weight > 500):
            errors.append("Weight must be a positive number between 0 and 500 kg")
        
        # Validate medical history
        medical_history = user_data.get("medical_history")
        if medical_history is not None and not isinstance(medical_history, dict):
            errors.append("Medical history must be a dictionary")
        
        # Validate medications
        medications = user_data.get("medications")
        if medications is not None and not isinstance(medications, list):
            errors.append("Medications must be a list")
        
        # Validate lifestyle factors
        lifestyle_factors = user_data.get("lifestyle_factors")
        if lifestyle_factors is not None and not isinstance(lifestyle_factors, dict):
            errors.append("Lifestyle factors must be a dictionary")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "error_count": len(errors),
            "warning_count": len(warnings)
        }