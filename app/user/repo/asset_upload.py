import math
import uuid
from typing import Sequence

from sqlalchemy import select, func, desc
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.asset_upload import CreateAsset, Metadata, FilterAsset
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.asset_upload import UploadedAsset
from app.utils.utils import generate_uuid, build_base_query


async def create_asset(
    db: AsyncSession,
    payload: CreateAsset
) -> UploadedAsset:
    db_uploaded_asset = UploadedAsset(
        id=generate_uuid(),
        user_id=payload.userId,
        file_name=payload.fileName,
        file_path=payload.filePath
    )

    try:
        db.add(db_uploaded_asset)
        await db.commit()
        await db.refresh(db_uploaded_asset)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_uploaded_asset


async def get_asset_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> UploadedAsset:
    query = build_base_query(UploadedAsset)
    query = query.filter(UploadedAsset.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_assets(
    db: AsyncSession,
    request: FilterAsset
) -> (Sequence[UploadedAsset], Metadata):
    query = (select(UploadedAsset))
    count_query = select(func.count(UploadedAsset.id))

    query = query.where(UploadedAsset.user_id == request.user_id)
    count_query = count_query.where(UploadedAsset.user_id == request.user_id)

    if request.asset_name:
        query = query.filter(UploadedAsset.file_name.ilike(f"%{request.asset_name}%"))
        count_query = count_query.filter(UploadedAsset.file_name.ilike(f"%{request.asset_name}%"))

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(UploadedAsset.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def delete_asset(
    db: AsyncSession,
    record_id: uuid.UUID,
) -> UploadedAsset:
    db_asset = await get_asset_by_id(db, record_id)

    if db_asset:
        await db.delete(db_asset)
        await db.commit()

    return db_asset


