import uuid
from datetime import datetime, timezone
from typing import Dict, Any

from sqlalchemy import UUID, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class GrapeJSProject(Base):
    __tablename__ = "tblGrapeJSProject"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    data: Mapped[Dict[str, Any]] = mapped_column(JSONB)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )







