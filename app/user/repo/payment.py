import uuid
from typing import Sequence

import math
from sqlalchemy import select, desc, func
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.payment import Payment
from app.schema.payment import CreatePayment, UpdatePaymentStatus, FilterPayment, Metadata
from app.utils.utils import generate_uuid, build_base_query


async def create_payment(
    db: AsyncSession,
    payload: CreatePayment
) -> Payment:
    db_payment = Payment(
        id=generate_uuid(),
        amount=payload.amount,
        reference=uuid.uuid4(),
        user_id=payload.user_id,
        narration=payload.narration,
        payment_nonce=payload.paymentNonce
    )

    try:
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_payment


async def get_payment_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Payment:
    query = build_base_query(Payment)
    query = query.filter(Payment.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def get_payment_by_reference(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Payment:
    query = build_base_query(Payment)
    query = query.filter(Payment.reference == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_payment(
    db: AsyncSession,
    request: FilterPayment
) -> (Sequence[Payment], Metadata):
    query = (select(Payment))
    count_query = select(func.count(Payment.id))

    if request.reference:
        query = query.filter(Payment.reference == request.reference)
        count_query = count_query.where(Payment.reference == request.reference)
    if request.user_id:
        query = query.filter(Payment.user_id == request.user_id)
        count_query = count_query.where(Payment.user_id == request.user_id)
    if request.payment_nonce:
        query = query.filter(Payment.nonce == request.payment_nonce)
        count_query = count_query.where(Payment.nonce == request.payment_nonce)
    if request.status:
        query = query.filter(Payment.status == request.status)
        count_query = count_query.where(Payment.status == request.status)

    size = request.size
    page = request.page

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / size)

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(Payment.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def update_payment_by_reference(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: UpdatePaymentStatus
) -> Payment:
    db_payment = await get_payment_by_reference(db, record_id)

    if db_payment:
        if payload.status:
            db_payment.status = payload.status
        if payload.externalReference:
            db_payment.external_reference = payload.externalReference

        await db.commit()
        await db.refresh(db_payment)

    return db_payment




