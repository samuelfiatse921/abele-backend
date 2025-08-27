import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.uploaded_template import APIResponseMetadata
from app.schema.user_template import APIResponse, CreateUserTemplate, FilterUserTemplate
from app.user.services.user_template import UserTemplateService
from app.utils.utils import generate_uuid_str, logger

user_template_router = APIRouter()


@user_template_router.post("")
async def create_user_template(
    payload: CreateUserTemplate,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new user template : {payload}")

    uploaded_template_svc = UserTemplateService(db, session_id)
    response = await uploaded_template_svc.create_user_template(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@user_template_router.get("/list")
async def list_user_templates(
    filter_query: Annotated[FilterUserTemplate, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering user(s) using payload : {filter_query}")

    uploaded_template_svc = UserTemplateService(db, session_id)
    response = await uploaded_template_svc.list_user_templates(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@user_template_router.delete("/{user_id}/template/{user_template_id}")
async def delete_user_template(
    user_id: uuid.UUID,
    user_template_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to delete template using id : {user_template_id}")

    user_template_svc = UserTemplateService(db, session_id)
    response = await user_template_svc.delete_user_template(user_template_id)

    logger.info(f"{session_id} - Response : {response}")

    return response



