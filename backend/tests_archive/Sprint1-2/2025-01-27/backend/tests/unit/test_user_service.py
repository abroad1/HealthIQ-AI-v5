"""
Unit tests for user service.
"""

import pytest
from unittest.mock import Mock, patch
from services.user_service import UserService
from core.models.user import User, UserContext


class TestUserService:
    """Test cases for UserService class."""
    
    @pytest.fixture
    def service(self):
        """Create a user service instance for testing."""
        return UserService()
    
    @pytest.fixture
    def sample_user_data(self):
        """Sample user data for testing."""
        return {
            "user_id": "test_user_123",
            "email": "test@example.com",
            "age": 35,
            "gender": "male",
            "height": 175.0,
            "weight": 70.0,
            "ethnicity": "caucasian",
            "medical_history": {"diabetes": False, "hypertension": False},
            "medications": ["vitamin_d", "omega_3"],
            "lifestyle_factors": {"exercise": "moderate", "smoking": False, "alcohol": "light"}
        }
    
    @pytest.mark.asyncio
    async def test_create_user_success(self, service, sample_user_data):
        """Test successful user creation."""
        user = await service.create_user(sample_user_data)
        
        assert isinstance(user, User)
        assert user.user_id == "test_user_123"
        assert user.email == "test@example.com"
        assert user.age == 35
        assert user.gender == "male"
        assert user.height == 175.0
        assert user.weight == 70.0
        assert user.ethnicity == "caucasian"
        assert user.medical_history == {"diabetes": False, "hypertension": False}
        assert user.medications == ["vitamin_d", "omega_3"]
        assert user.lifestyle_factors == {"exercise": "moderate", "smoking": False, "alcohol": "light"}
        assert user.created_at is not None
        assert user.updated_at is not None
    
    @pytest.mark.asyncio
    async def test_create_user_generate_id(self, service):
        """Test user creation with auto-generated ID."""
        user_data = {
            "email": "test@example.com",
            "age": 25
        }
        
        user = await service.create_user(user_data)
        
        assert user.user_id is not None
        assert len(user.user_id) > 0
        assert user.email == "test@example.com"
        assert user.age == 25
    
    @pytest.mark.asyncio
    async def test_create_user_minimal_data(self, service):
        """Test user creation with minimal data."""
        user_data = {"user_id": "minimal_user"}
        
        user = await service.create_user(user_data)
        
        assert user.user_id == "minimal_user"
        assert user.email is None
        assert user.age is None
        assert user.medical_history == {}
        assert user.medications == []
        assert user.lifestyle_factors == {}
    
    @pytest.mark.asyncio
    async def test_get_user_found(self, service, sample_user_data):
        """Test getting an existing user."""
        created_user = await service.create_user(sample_user_data)
        retrieved_user = await service.get_user("test_user_123")
        
        assert retrieved_user is not None
        assert retrieved_user.user_id == created_user.user_id
        assert retrieved_user.email == created_user.email
    
    @pytest.mark.asyncio
    async def test_get_user_not_found(self, service):
        """Test getting a non-existent user."""
        user = await service.get_user("nonexistent_user")
        assert user is None
    
    @pytest.mark.asyncio
    async def test_update_user_success(self, service, sample_user_data):
        """Test successful user update."""
        created_user = await service.create_user(sample_user_data)
        
        update_data = {
            "age": 36,
            "weight": 72.0,
            "medications": ["vitamin_d", "omega_3", "magnesium"]
        }
        
        updated_user = await service.update_user("test_user_123", update_data)
        
        assert updated_user is not None
        assert updated_user.user_id == "test_user_123"
        assert updated_user.age == 36  # Updated
        assert updated_user.weight == 72.0  # Updated
        assert updated_user.email == "test@example.com"  # Unchanged
        assert updated_user.medications == ["vitamin_d", "omega_3", "magnesium"]  # Updated
        assert updated_user.updated_at != created_user.updated_at
    
    @pytest.mark.asyncio
    async def test_update_user_not_found(self, service):
        """Test updating a non-existent user."""
        update_data = {"age": 36}
        updated_user = await service.update_user("nonexistent_user", update_data)
        assert updated_user is None
    
    @pytest.mark.asyncio
    async def test_delete_user_success(self, service, sample_user_data):
        """Test successful user deletion."""
        await service.create_user(sample_user_data)
        
        # Verify user exists
        user = await service.get_user("test_user_123")
        assert user is not None
        
        # Delete user
        deleted = await service.delete_user("test_user_123")
        assert deleted is True
        
        # Verify user is gone
        user = await service.get_user("test_user_123")
        assert user is None
    
    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, service):
        """Test deleting a non-existent user."""
        deleted = await service.delete_user("nonexistent_user")
        assert deleted is False
    
    @pytest.mark.asyncio
    async def test_list_users_empty(self, service):
        """Test listing users when none exist."""
        users = await service.list_users()
        assert users == []
    
    @pytest.mark.asyncio
    async def test_list_users_with_pagination(self, service):
        """Test listing users with pagination."""
        # Create multiple users
        for i in range(5):
            user_data = {
                "user_id": f"user_{i}",
                "email": f"user{i}@example.com",
                "age": 20 + i
            }
            await service.create_user(user_data)
        
        # Test pagination
        users_page1 = await service.list_users(limit=3, offset=0)
        assert len(users_page1) == 3
        
        users_page2 = await service.list_users(limit=3, offset=3)
        assert len(users_page2) == 2
        
        # Verify users are sorted by creation date (newest first)
        assert users_page1[0].user_id == "user_4"  # Most recent
    
    @pytest.mark.asyncio
    async def test_validate_user_data_valid(self, service):
        """Test validating valid user data."""
        valid_data = {
            "email": "valid@example.com",
            "age": 30,
            "gender": "female",
            "height": 165.0,
            "weight": 60.0,
            "medical_history": {"diabetes": False},
            "medications": ["vitamin_c"],
            "lifestyle_factors": {"exercise": "daily"}
        }
        
        result = await service.validate_user_data(valid_data)
        
        assert result["valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_email(self, service):
        """Test validating user data with invalid email."""
        invalid_data = {
            "email": "invalid-email",
            "age": 30
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Invalid email format" in result["errors"]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_age(self, service):
        """Test validating user data with invalid age."""
        invalid_data = {
            "email": "test@example.com",
            "age": 200  # Invalid age
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Age must be a valid integer" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_height(self, service):
        """Test validating user data with invalid height."""
        invalid_data = {
            "email": "test@example.com",
            "height": -10.0  # Invalid height
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Height must be a positive number" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_weight(self, service):
        """Test validating user data with invalid weight."""
        invalid_data = {
            "email": "test@example.com",
            "weight": 1000.0  # Invalid weight
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Weight must be a positive number" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_warning_gender(self, service):
        """Test validating user data with non-standard gender."""
        data_with_warning = {
            "email": "test@example.com",
            "gender": "non_binary"  # Non-standard but not invalid
        }
        
        result = await service.validate_user_data(data_with_warning)
        
        assert result["valid"] is True  # Should still be valid
        assert len(result["warnings"]) == 1
        assert "Gender value not in standard options" in result["warnings"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_medical_history(self, service):
        """Test validating user data with invalid medical history."""
        invalid_data = {
            "email": "test@example.com",
            "medical_history": "not_a_dict"  # Should be a dict
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Medical history must be a dictionary" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_medications(self, service):
        """Test validating user data with invalid medications."""
        invalid_data = {
            "email": "test@example.com",
            "medications": "not_a_list"  # Should be a list
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Medications must be a list" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_invalid_lifestyle_factors(self, service):
        """Test validating user data with invalid lifestyle factors."""
        invalid_data = {
            "email": "test@example.com",
            "lifestyle_factors": "not_a_dict"  # Should be a dict
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) == 1
        assert "Lifestyle factors must be a dictionary" in result["errors"][0]
    
    @pytest.mark.asyncio
    async def test_validate_user_data_multiple_errors(self, service):
        """Test validating user data with multiple errors."""
        invalid_data = {
            "email": "invalid-email",
            "age": 200,
            "height": -10.0,
            "weight": 1000.0,
            "medical_history": "not_a_dict",
            "medications": "not_a_list"
        }
        
        result = await service.validate_user_data(invalid_data)
        
        assert result["valid"] is False
        assert len(result["errors"]) >= 5  # Multiple errors
        assert result["error_count"] >= 5