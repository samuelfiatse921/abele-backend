import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.schema.enums import Gender, Status
from app.user.models.base import Base


class User(Base):
    __tablename__ = "tblUsers"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(10), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    street_number: Mapped[str] = mapped_column(String(10), nullable=False)
    street_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True, index=True)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)
    postcode: Mapped[str] = mapped_column(String(50), nullable=False)
    longitude: Mapped[str] = mapped_column(String(10), nullable=True, default="")
    latitude: Mapped[str] = mapped_column(String(10), nullable=True, default="")
    timezone_offset: Mapped[str] = mapped_column(String(6), nullable=True, default="")
    timezone_description: Mapped[str] = mapped_column(String(50), nullable=True, default="")
    dob: Mapped[str] = mapped_column(String(10), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False, unique=True, index=True)
    cell: Mapped[str] = mapped_column(String(15), nullable=False)
    nat: Mapped[str] = mapped_column(String(5), nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender, name="gender"), unique=False, nullable=False)
    picture_large: Mapped[str] = mapped_column(String(100), nullable=False)
    picture_medium: Mapped[str] = mapped_column(String(100), nullable=False)
    picture_thumbnail: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[Status] = mapped_column(Enum(Status, name="user_status"), nullable=False, default=Status.ACTIVE)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )
