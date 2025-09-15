import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class GrapeJSProject(Base):
    __tablename__ = "tblGrapeJSProject"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    data: Mapped[list[dict]] = mapped_column(JSONB)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'template_id', name='uq_user_id_template_id'),
    )







