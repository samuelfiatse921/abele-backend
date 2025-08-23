import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth.deps import get_current_user
from app.deps.db.db import get_db_session
from app.schema.user import CreateUser, APIResponse, FilterUser, APIResponseMetadata, UpdateUser, GetUserCredentials
from app.user.services.user import UserService
from app.utils.utils import generate_uuid_str, logger

user_router = APIRouter()


@user_router.post("")
async def create_user(
    payload: CreateUser,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new user : {payload}")

    user_svc = UserService(db, session_id)
    response = await user_svc.create(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@user_router.get("/single/{record_id}")
async def get_single_user(
    record_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to get a single user using id : {record_id}")

    user_svc = UserService(db, session_id)
    response = await user_svc.get_one_user(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@user_router.get("/list")
async def list_users(
    filter_query: Annotated[FilterUser, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering user(s) using payload : {filter_query}")

    user_svc = UserService(db, session_id)
    response = await user_svc.list_users(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@user_router.put("/{record_id}/from-user/{user_id}")
async def update_user(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    payload: UpdateUser,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to update user using payload : {payload}")

    user_svc = UserService(db, session_id)
    response = await user_svc.update_user(record_id, payload)

    logger.info(f"{session_id} - Response : {response}")

    return response



