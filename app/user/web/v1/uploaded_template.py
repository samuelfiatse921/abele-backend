import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.auth.deps import get_current_user
from app.deps.db.db import get_db_session
from app.schema.uploaded_template import CreateUploadedTemplate, APIResponse, FilterUploadedTemplate, \
    APIResponseMetadata, UpdateUploadedTemplate, SingleRecordAPIResponse
from app.schema.user import GetUserCredentials
from app.user.services.uploaded_template import TemplateUploadService
from app.utils.utils import generate_uuid_str, logger

template_upload_router = APIRouter()


@template_upload_router.post("")
async def create_uploaded_template(
    payload: CreateUploadedTemplate,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new uploaded template : {payload}")

    uploaded_template_svc = TemplateUploadService(db, session_id)
    response = await uploaded_template_svc.create_uploaded_template(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@template_upload_router.get("/single/{record_id}")
async def get_single_uploaded_template(
    record_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> SingleRecordAPIResponse:
    logger.info(f"{session_id} - Request received to get an uploaded template using id : {record_id}")

    uploaded_template_svc = TemplateUploadService(db, session_id)
    response = await uploaded_template_svc.get_one_uploaded_template(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@template_upload_router.get("/list")
async def list_uploaded_templates(
    filter_query: Annotated[FilterUploadedTemplate, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering uploaded template(s) using payload : {filter_query}")

    uploaded_template_svc = TemplateUploadService(db, session_id)
    response = await uploaded_template_svc.list_uploaded_templates(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@template_upload_router.put("/{record_id}/from-user/{user_id}")
async def update_uploaded_template(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    payload: UpdateUploadedTemplate,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to update uploaded template using payload : {payload}")

    uploaded_template_svc = TemplateUploadService(db, session_id)
    response = await uploaded_template_svc.update_uploaded_template(record_id, payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@template_upload_router.delete("/{record_id}/from-user/{user_id}")
async def delete_uploaded_template(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
    authenticated_user: GetUserCredentials = Depends(get_current_user)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to delete uploaded template using id : {record_id}")

    uploaded_template_svc = TemplateUploadService(db, session_id)
    response = await uploaded_template_svc.delete_uploaded_template(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response









