import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class UploadedAsset(Base):
    __tablename__ = "tblUploadedAssets"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=False, index=True)
    file_name: Mapped[str] = mapped_column(String(100), nullable=False)
    file_path: Mapped[str] = mapped_column(String(180), nullable=False)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )



