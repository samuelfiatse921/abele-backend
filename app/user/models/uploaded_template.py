import uuid
from datetime import datetime, timezone

from sqlalchemy import UUID, DateTime, Enum, String, ARRAY, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.schema.enums import TemplateCategory, TemplateTier, TemplateUnder
from app.user.models.base import Base


class UploadedTemplate(Base):
    __tablename__ = "tblUploadedTemplates"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False, unique=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    coin: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    image: Mapped[str] = mapped_column(String(100), nullable=False)
    tier: Mapped[TemplateTier] = mapped_column(Enum(TemplateTier, name="template_tier"), unique=False, nullable=False)
    category: Mapped[TemplateCategory] = mapped_column(Enum(TemplateCategory, name="template_category"), unique=False, nullable=False)
    under: Mapped[TemplateUnder] = mapped_column(Enum(TemplateUnder, name="template_under"), unique=False, nullable=False)
    live_demo: Mapped[str] = mapped_column(String(150), nullable=False)
    html_files: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    css_files: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    js_files: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    reviews: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    rating: Mapped[int] = mapped_column(Integer, nullable=True, default=0)
    created_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True
    )
    updated_on: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        index=True
    )


