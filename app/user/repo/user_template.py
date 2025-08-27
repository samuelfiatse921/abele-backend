import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func, Row
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.uploaded_template import Metadata
from app.schema.user_template import CreateUserTemplate, FilterUserTemplate
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.uploaded_template import UploadedTemplate
from app.user.models.user import User
from app.user.models.user_template import UserTemplate
from app.utils.utils import generate_uuid, build_base_query


async def create_user_template(
    db: AsyncSession,
    payload: CreateUserTemplate
) -> UserTemplate:
    db_user_template = UserTemplate(
        id=generate_uuid(),
        template_id=payload.templateId,
        user_id=payload.userId
    )

    try:
        db.add(db_user_template)
        await db.commit()
        await db.refresh(db_user_template)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_user_template


async def get_user_template_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> UserTemplate:
    query = build_base_query(UserTemplate)
    query = query.filter(UserTemplate.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_user_template(
    db: AsyncSession,
    request: FilterUserTemplate
) -> tuple[Sequence[Row[tuple[UploadedTemplate, User, UserTemplate]]], Metadata]:
    query = (
        select(UploadedTemplate, User, UserTemplate)
        .join(User, UploadedTemplate.owner_id == User.id)  # UploadedTemplate → User
        .join(UserTemplate, UserTemplate.template_id == UploadedTemplate.id)  # User → UserTemplate
        .where(UserTemplate.user_id == request.userId)
    )

    count_query = (
        select(func.count(UploadedTemplate.id))
        .join(User, UploadedTemplate.owner_id == User.id)  # UploadedTemplate → User
        .join(UserTemplate, UserTemplate.template_id == UploadedTemplate.id)  # User → UserTemplate
        .where(UserTemplate.user_id == request.userId)
    )

    if request.templateId:
        query = query.where(UserTemplate.template_id == request.templateId)
        count_query = count_query.where(UserTemplate.template_id == request.templateId)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(UploadedTemplate.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.all(), metadata


async def delete_user_template(
    db: AsyncSession,
    record_id: uuid.UUID,
) -> UserTemplate:
    db_user_template = await get_user_template_by_id(db, record_id)

    if db_user_template:
        await db.delete(db_user_template)
        await db.commit()

    return db_user_template


