import math
import uuid
from typing import Sequence

from sqlalchemy import select, func, desc
from sqlalchemy.exc import OperationalError, DataError
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.deployment import CreateDeployment, Metadata, FilterDeployments, UpdateDeployment
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.models.deployment import Deployment
from app.utils.utils import generate_uuid, build_base_query


async def create_deployment(
    db: AsyncSession,
    payload: CreateDeployment
) -> Deployment:
    db_deployment = Deployment(
        id=generate_uuid(),
        name=payload.name,
        deployment_support_cost=payload.deploymentSupportCost,
        deployment_support_description=payload.deploymentSupportDescription,
        domain_support_cost=payload.domainSupportCost,
        domain_support_description=payload.domainSupportDescription
    )

    try:
        db.add(db_deployment)
        await db.commit()
        await db.refresh(db_deployment)
    except (OperationalError, DataError):
        raise DatabaseException("Database operation failed")

    return db_deployment


async def get_deployment_by_id(
    db: AsyncSession,
    record_id: uuid.UUID
) -> Deployment:
    query = build_base_query(Deployment)
    query = query.filter(Deployment.id == record_id)
    record_found = await db.execute(query)

    return record_found.scalars().first()


async def filter_deployment(
    db: AsyncSession,
    request: FilterDeployments
) -> (Sequence[Deployment], Metadata):
    query = (select(Deployment))
    count_query = select(func.count(Deployment.id))

    if request.name:
        query = query.filter(Deployment.name == request.name)
        count_query = count_query.where(Deployment.name == request.name)

    count_result = await db.execute(count_query)
    total = count_result.scalar()
    total_pages = math.ceil(total / request.size)

    page = request.page
    size = request.size

    offset = (page - 1) * size
    query = query.offset(offset).limit(size).order_by(desc(Deployment.created_on))
    result = await db.execute(query)

    metadata = Metadata(page=page, results=size, totalPages=total_pages)

    return result.scalars().all(), metadata


async def update_deployment(
    db: AsyncSession,
    record_id: uuid.UUID,
    payload: UpdateDeployment
) -> Deployment:
    db_deployment = await get_deployment_by_id(db, record_id)

    if db_deployment:
        if payload.name:
            db_deployment.name = payload.name
        if payload.deploymentSupportCost:
            db_deployment.deployment_support_cost = payload.deploymentSupportCost
        if payload.deploymentSupportDescription:
            db_deployment.deployment_support_description = payload.deploymentSupportDescription
        if payload.domainSupportCost:
            db_deployment.domain_support_cost = payload.domainSupportCost
        if payload.domainSupportDescription:
            db_deployment.domain_support_description = payload.domainSupportDescription

        await db.commit()
        await db.refresh(db_deployment)

    return db_deployment


async def delete_deployment(
    db: AsyncSession,
    record_id: uuid.UUID,
) -> Deployment:
    db_deployment = await get_deployment_by_id(db, record_id)

    if db_deployment:
        await db.delete(db_deployment)
        await db.commit()

    return db_deployment




