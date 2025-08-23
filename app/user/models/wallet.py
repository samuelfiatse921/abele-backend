import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, Float, Enum
from sqlalchemy.orm import Mapped, mapped_column

from app.schema.enums import Status
from app.user.models.base import Base


class Wallet(Base):
    __tablename__ = "tblWallets"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=True, index=True)
    balance: Mapped[int] = mapped_column(Float, nullable=False, default=0)
    status: Mapped[Status] = mapped_column(Enum(Status, name="user_status"), nullable=False, default=Status.ACTIVE)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )





