import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.following import CreateFollowing, FilterFollowings, FilterFollowers
from app.schema.user import Metadata
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.following import Following
from app.user.models.user import User
from app.utils.utils import generate_uuid, build_base_query


async def create_following(
    db: AsyncSession,
    payload: CreateFollowing
) -> Following:
    db_following = Following(
        id=generate_uuid(),
        user_id=payload.userId,
        following_user_id=payload.followingUserId
    )

    try:
        db.add(db_following)
        await db.commit()
        await db.refresh(db_following)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_following


async def get_following_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Following:
    query = build_base_query(Following)
    query = query.filter(Following.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_followings(
    db: AsyncSession,
    request: FilterFollowings
) -> (Sequence[User], Metadata):
    template_cond = User.id == Following.following_user_id
    query = (select(User)).join(Following, template_cond)
    count_query = select(func.count(User.id)).join(Following, template_cond)

    query = query.where(Following.user_id == request.userId)
    count_query = count_query.where(Following.user_id == request.userId)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(User.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def filter_followers(
    db: AsyncSession,
    request: FilterFollowers
) -> (Sequence[User], Metadata):
    template_cond = User.id == Following.user_id
    query = (select(User)).join(Following, template_cond)
    count_query = select(func.count(User.id)).join(Following, template_cond)

    query = query.where(Following.following_user_id == request.userId)
    count_query = count_query.where(Following.following_user_id == request.userId)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(User.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def unfollower_user_by_id(
    db: AsyncSession,
    record_id: uuid.UUID,
) -> Following:
    db_following = await get_following_by_id(db, record_id)

    if db_following:
        await db.delete(db_following)
        await db.commit()

    return db_following





