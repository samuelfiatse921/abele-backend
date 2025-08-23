import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, Enum, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.schema.enums import PaymentStatus
from app.user.models.base import Base


class Payment(Base):
    __tablename__ = "tblPayments"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    currency: Mapped[str] = mapped_column(String(5), nullable=False, default="USD")
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    reference: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=True, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=False, index=True)
    payment_nonce: Mapped[str] = mapped_column(String(100), nullable=True, unique=False, index=True, default=None)
    external_reference: Mapped[str] = mapped_column(String(100), nullable=True, unique=False, index=True, default=None)
    narration: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        unique=False,
        nullable=False,
        index=True,
        default=PaymentStatus.PENDING
    )
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )
