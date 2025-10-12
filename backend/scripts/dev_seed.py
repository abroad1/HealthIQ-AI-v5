"""
Development seed script for creating default test user profile.
This ensures the analysis flow can work even without full auth implementation.
"""

import sys
from pathlib import Path

# Add backend directory to path for imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from uuid import UUID
import logging
from sqlalchemy.orm import Session

from core.models.database import Profile
from config.database import get_db

logger = logging.getLogger(__name__)

# Default dev user ID (consistent across restarts)
DEV_USER_ID = UUID("5029514b-f7fd-4dff-8d60-4fb8b7f90dd4")
DEV_USER_EMAIL = "dev@healthiq.ai"


def seed_dev_user() -> None:
    """
    Seed a default developer user profile for testing.
    Safe to run multiple times - checks if profile already exists.
    """
    try:
        db: Session = next(get_db())
        
        # Check if dev user already exists
        existing = db.query(Profile).filter(Profile.user_id == DEV_USER_ID).first()
        
        if existing:
            logger.info(f"[DEV SEED] Developer profile already exists: {DEV_USER_EMAIL}")
            return
        
        # Create new dev profile
        dev_profile = Profile(
            user_id=DEV_USER_ID,
            email=DEV_USER_EMAIL,
            demographics={
                "age": 35,
                "sex": "male",
                "height": 180,
                "weight": 75
            },
            consent_given=True,
            consent_version="1.0"
        )
        
        db.add(dev_profile)
        db.commit()
        
        logger.info(f"[DEV SEED] ✅ Default developer profile created: {DEV_USER_EMAIL}")
        logger.info(f"[DEV SEED] User ID: {DEV_USER_ID}")
        
    except Exception as e:
        logger.error(f"[DEV SEED] Failed to seed developer profile: {str(e)}")
        # Don't crash the app if seeding fails
    finally:
        db.close()


if __name__ == "__main__":
    # Can be run standalone for testing
    logging.basicConfig(level=logging.INFO)
    seed_dev_user()

