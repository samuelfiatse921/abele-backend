import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth import deps
from app.schema.user import CreateUser, FilterUser, UpdateUser, Metadata
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.user import User
from app.utils.utils import generate_uuid, build_base_query, get_country_code


async def create_user(
    db: AsyncSession,
    payload: CreateUser
) -> User:
    db_user = User(
        id=generate_uuid(),
        username=payload.username,
        title=payload.title,
        first_name=payload.firstName,
        last_name=payload.lastName,
        street_number=payload.streetNumber,
        street_name=payload.streetName,
        email=payload.email,
        city=payload.city,
        state=payload.state,
        country=get_country_code(payload.country),
        postcode=payload.postcode,
        longitude=payload.longitude,
        latitude=payload.latitude,
        timezone_offset=payload.timezoneOffset,
        timezone_description=payload.timezoneDescription,
        dob=payload.dob,
        phone=payload.phone,
        cell=payload.cell,
        nat=payload.nat,
        gender=payload.gender,
        picture_large=payload.pictureLarge,
        picture_medium=payload.pictureMedium,
        picture_thumbnail=payload.pictureThumbnail,
        hashed_password=deps.get_password_hash(password=payload.password)
    )

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_user


async def get_user_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> User:
    query = build_base_query(User)
    query = query.filter(User.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_user_by_username(
    db: AsyncSession,
    username: str
) -> User:
    query = build_base_query(User)
    query = query.filter(User.username == username)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_user_by_email(
    db: AsyncSession,
    email: str
) -> User:
    query = build_base_query(User)
    query = query.filter(User.email == email)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_user_by_phone_number(
    db: AsyncSession,
    phone_number: str
) -> User:
    query = build_base_query(User)
    query = query.filter(User.phone == phone_number)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_users(
    db: AsyncSession,
    request: FilterUser
) -> (Sequence[User], Metadata):
    query = (select(User))
    count_query = select(func.count(User.id))

    if request.username:
        query = query.filter(User.username == request.username)
        count_query = count_query.where(User.username == request.username)
    if request.firstName:
        query = query.filter(User.firstName == request.firstName)
        count_query = count_query.where(User.first_name == request.firstName)
    if request.lastName:
        query = query.filter(User.last_name == request.lastName)
        count_query = count_query.where(User.last_name == request.lastName)
    if request.city:
        query = query.filter(User.city == request.city)
        count_query = count_query.where(User.city == request.city)
    if request.state:
        query = query.filter(User.state == request.state)
        count_query = count_query.where(User.state == request.state)
    if request.country:
        query = query.filter(User.country == request.country)
        count_query = count_query.where(User.country == request.country)
    if request.gender:
        query = query.filter(User.gender == request.gender)
        count_query = count_query.where(User.gender == request.gender)
    if request.status:
        query = query.filter(User.status == request.status)
        count_query = count_query.where(User.status == request.status)

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


async def update_user_by_id(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: UpdateUser
) -> User:
    db_user = await get_user_by_id(db, record_id)

    if db_user:
        if payload.title:
            db_user.title = payload.title
        if payload.username:
            db_user.username = payload.username
        if payload.firstName:
            db_user.first_name = payload.firstName
        if payload.lastName:
            db_user.last_name = payload.lastName
        if payload.streetName:
            db_user.street_name = payload.streetName
        if payload.streetNumber:
            db_user.street_number = payload.streetNumber
        if payload.email:
            db_user.email = payload.email
        if payload.city:
            db_user.city = payload.city
        if payload.state:
            db_user.state = payload.state
        if payload.country:
            db_user.country = payload.country
        if payload.postcode:
            db_user.postcode = payload.postcode
        if payload.longitude:
            db_user.longitude = payload.longitude
        if payload.latitude:
            db_user.latitude = payload.latitude
        if payload.timezoneOffset:
            db_user.timezoneOffset = payload.timezoneOffset
        if payload.timezoneDescription:
            db_user.timezoneDescription = payload.timezoneDescription
        if payload.dob:
            db_user.dob = payload.dob
        if payload.phone:
            db_user.phone = payload.phone
        if payload.gender:
            db_user.gender = payload.phone
        if payload.pictureLarge:
            db_user.pictureLarge = payload.pictureLarge
        if payload.pictureMedium:
            db_user.pictureMedium = payload.pictureMedium
        if payload.pictureThumbnail:
            db_user.pictureThumbnail = payload.pictureThumbnail

        await db.commit()
        await db.refresh(db_user)

    return db_user

