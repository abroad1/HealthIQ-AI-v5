from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from core.models.database import Export  # existing ORM model

class ExportRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, **kwargs) -> Export:
        """Create a new export record."""
        exp = Export(
            id=uuid4(),
            analysis_id=kwargs.get("analysis_id"),
            user_id=kwargs.get("user_id"),
            export_type=kwargs.get("export_type", "json").lower(),
            status=kwargs.get("status", "pending"),
            storage_path=kwargs.get("file_path"),
            file_size_bytes=kwargs.get("file_size_bytes"),
            completed_at=datetime.utcnow() if kwargs.get("status") == "ready" else None,
        )
        self.db.add(exp)
        self.db.commit()
        self.db.refresh(exp)
        return exp

    def create_completed(
        self,
        *,
        analysis_id: UUID,
        user_id: UUID,
        format: str,
        storage_path: str,
        file_size_bytes: int
    ) -> Export:
        exp = Export(
            id=uuid4(),
            analysis_id=analysis_id,
            user_id=user_id,
            export_type=format.lower(),
            status="ready",
            storage_path=storage_path,
            file_size_bytes=file_size_bytes,
            completed_at=datetime.utcnow(),
        )
        self.db.add(exp)
        self.db.commit()
        self.db.refresh(exp)
        return exp

    def get_by_id_for_user(self, *, export_id: UUID, user_id: UUID) -> Optional[Export]:
        stmt = select(Export).where(Export.id == export_id, Export.user_id == user_id)
        return self.db.execute(stmt).scalars().first()