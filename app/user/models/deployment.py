import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.user.models.base import Base


class Deployment(Base):
    __tablename__ = "tblDeployments"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    deployment_support_cost: Mapped[float] = mapped_column(Float, nullable=False)
    deployment_support_description: Mapped[String] = mapped_column(String(150), nullable=True, default="")
    domain_support_cost: Mapped[float] = mapped_column(Float, nullable=False)
    domain_support_description: Mapped[String] = mapped_column(String(150), nullable=True, default="")
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )


