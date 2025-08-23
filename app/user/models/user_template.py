import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class UserTemplate(Base):
    __tablename__ = "tblUserTemplates"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, index=True)
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
        UniqueConstraint('template_id', 'user_id', name='uq_template_id_user_id'),
    )


