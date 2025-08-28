import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth.deps import get_current_user
from app.deps.db.db import get_db_session
from app.schema.deployment import CreateDeployment, APIResponse, FilterDeployments, APIResponseMetadata, \
    UpdateDeployment
from app.schema.user import GetUserCredentials
from app.user.services.deployment import DeploymentService
from app.utils.utils import generate_uuid_str, logger

deployment_router = APIRouter()


@deployment_router.post("")
async def create_deployment(
    payload: CreateDeployment,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new deployment : {payload}")

    deployment_svc = DeploymentService(db, session_id)
    response = await deployment_svc.create_deployment(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@deployment_router.get("/single/{record_id}")
async def get_single_deployment(
    record_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to get a single deployment using id : {record_id}")

    deployment_svc = DeploymentService(db, session_id)
    response = await deployment_svc.get_one_deployment(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@deployment_router.get("/list")
async def list_deployments(
    filter_query: Annotated[FilterDeployments, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering deployment(s) using payload : {filter_query}")

    deployment_svc = DeploymentService(db, session_id)
    response = await deployment_svc.list_deployments(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@deployment_router.put("/{record_id}/from-user/{user_id}")
async def update_user(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    payload: UpdateDeployment,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to update deployment using payload : {payload}")

    deployment_svc = DeploymentService(db, session_id)
    response = await deployment_svc.update_deployment(record_id, payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@deployment_router.delete("/{record_id}/from-user/{user_id}")
async def delete_deployment(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to delete deployment : {record_id}")

    deployment_svc = DeploymentService(db, session_id)
    response = await deployment_svc.delete_deployment(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


