import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class Following(Base):
    __tablename__ = "tblFollowings"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=False, index=True)
    following_user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=False, index=True)
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
        UniqueConstraint('user_id', 'following_user_id', name='uq_user_id_following_user_id'),
    )

