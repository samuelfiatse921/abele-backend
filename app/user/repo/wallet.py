import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.wallet import CreateWallet, FilterWallet, CreditWallet, DebitWallet, UpdateWalletStatus, Metadata
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.wallet import Wallet
from app.utils.utils import generate_uuid, build_base_query


async def create_wallet(
    db: AsyncSession,
    payload: CreateWallet
) -> Wallet:
    db_wallet = Wallet(
        id=generate_uuid(),
        user_id=payload.userId,
        balance=payload.balance
    )

    try:
        db.add(db_wallet)
        await db.commit()
        await db.refresh(db_wallet)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_wallet


async def get_wallet_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Wallet:
    query = build_base_query(Wallet)
    query = query.filter(Wallet.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_wallet_by_user_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Wallet:
    query = build_base_query(Wallet)
    query = query.filter(Wallet.user_id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_wallets(
    db: AsyncSession,
    request: FilterWallet
) -> (Sequence[Wallet], Metadata):
    query = (select(Wallet))
    count_query = select(func.count(Wallet.id))

    if request.userId:
        query = query.filter(Wallet.user_id == request.userId)
        count_query = count_query.where(Wallet.user_id == request.userId)
    if request.status:
        query = query.filter(Wallet.status == request.status)
        count_query = count_query.where(Wallet.status == request.status)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(Wallet.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def credit_wallet(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: CreditWallet
) -> Wallet:
    db_wallet = await get_wallet_by_user_id(db, record_id)

    if db_wallet:
        db_wallet.balance = db_wallet.balance + payload.amount

        await db.commit()
        await db.refresh(db_wallet)

    return db_wallet


async def debit_wallet(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: DebitWallet
) -> Wallet:
    db_wallet = await get_wallet_by_user_id(db, record_id)

    if db_wallet:
        db_wallet.balance = db_wallet.balance - payload.amount

        await db.commit()
        await db.refresh(db_wallet)

    return db_wallet


async def update_wallet_status(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: UpdateWalletStatus
) -> Wallet:
    db_wallet = await get_wallet_by_id(db, record_id)

    if db_wallet:
        db_wallet.status = payload.status

        await db.commit()
        await db.refresh(db_wallet)

    return db_wallet





