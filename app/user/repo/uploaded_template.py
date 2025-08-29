import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func, Row, exists
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.uploaded_template import CreateUploadedTemplate, FilterUploadedTemplate, UpdateUploadedTemplate, \
    Metadata
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.uploaded_template import UploadedTemplate
from app.user.models.user import User
from app.user.models.user_template import UserTemplate
from app.utils.utils import generate_uuid, build_base_query


async def create_uploaded_template(
    db: AsyncSession,
    payload: CreateUploadedTemplate
) -> UploadedTemplate:
    template_files = payload.files
    db_uploaded_template = UploadedTemplate(
        id=generate_uuid(),
        owner_id=payload.ownerId,
        name=payload.name,
        price=payload.price,
        coin=payload.coin,
        image=payload.image,
        tier=payload.tier,
        category=payload.category,
        under=payload.under,
        live_demo=payload.liveDemo,
        html_files=template_files.htmlFiles,
        css_files=template_files.cssFiles,
        js_files=template_files.jsFiles
    )

    try:
        db.add(db_uploaded_template)
        await db.commit()
        await db.refresh(db_uploaded_template)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_uploaded_template


def build_join_query():
    template_cond = UploadedTemplate.owner_id == User.id
    query = (select(UploadedTemplate, User).join(User, template_cond))
    count_query = select(func.count(UploadedTemplate.id)).join(User, template_cond)
    return query, count_query


async def get_uploaded_template_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> UploadedTemplate:
    query = build_base_query(UploadedTemplate)
    query = query.filter(UploadedTemplate.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_joined_uploaded_template_and_user_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Sequence[Row[tuple[UploadedTemplate, User]]]:
    query, _ = build_join_query()
    query = query.where(UploadedTemplate.id == record_id)
    record_found = await db.execute(query)

    return record_found.all()


async def filter_uploaded_template(
    db: AsyncSession,
    request: FilterUploadedTemplate
) -> tuple[Sequence[Row[tuple[UploadedTemplate, User]]], Metadata]:
    query, count_query = build_join_query()

    if request.name:
        query = query.filter(UploadedTemplate.name.ilike(f"%{request.name}%"))
        count_query = count_query.filter(UploadedTemplate.name.ilike(f"%{request.name}%"))
    if request.ownerId:
        query = query.where(UploadedTemplate.owner_id == request.ownerId)
        count_query = count_query.where(UploadedTemplate.owner_id == request.ownerId)
    if request.userId:
        subq = (
            select(UserTemplate.id)
            .where(UserTemplate.template_id == UploadedTemplate.id)
            .where(UserTemplate.user_id == request.userId)
        )
        query = query.where(~exists(subq))
        count_query = count_query.where(~exists(subq))
    if request.tier:
        query = query.where(UploadedTemplate.tier == request.tier)
        count_query = count_query.where(UploadedTemplate.tier == request.tier)
    if request.category:
        query = query.where(UploadedTemplate.category == request.category)
        count_query = count_query.where(UploadedTemplate.category == request.category)
    if request.under:
        query = query.where(UploadedTemplate.under == request.under)
        count_query = count_query.where(UploadedTemplate.under == request.under)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(User.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.all(), metadata


async def update_uploaded_template_by_id(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: UpdateUploadedTemplate
) -> UploadedTemplate:
    db_uploaded_template = await get_uploaded_template_by_id(db, record_id)

    if db_uploaded_template:
        if payload.image_path:
            db_uploaded_template.image = payload.image_path
        if payload.price:
            db_uploaded_template.price = payload.price
        if payload.type:
            db_uploaded_template.tier = payload.type
        if payload.category:
            db_uploaded_template.category = payload.category
        if payload.htmlFiles:
            db_uploaded_template.htmlFiles = payload.htmlFiles
        if payload.cssFiles:
            db_uploaded_template.cssFiles = payload.cssFiles
        if payload.jsFiles:
            db_uploaded_template.jsFiles = payload.jsFiles

        await db.commit()
        await db.refresh(db_uploaded_template)

    return db_uploaded_template


async def delete_uploaded_template_by_id(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> UploadedTemplate:
    db_uploaded_template = await get_uploaded_template_by_id(db, user_id)

    if db_uploaded_template:
        await db.delete(db_uploaded_template)
        await db.commit()

    return db_uploaded_template


