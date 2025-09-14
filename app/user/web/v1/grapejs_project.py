import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.grapejs_project import CreateProject, APIResponse
from app.user.services.grapejs_project import GrapeJSService
from app.utils.utils import generate_uuid_str, logger

grape_js_router = APIRouter()


@grape_js_router.post("")
async def create_project(
    payload: CreateProject,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new grape-js project : {payload}")

    svc = GrapeJSService(db, session_id)
    response = await svc.create_grape_js_project(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@grape_js_router.get("/single/{record_id}")
async def get_single_project(
    record_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to get a single project using id : {record_id}")

    svc = GrapeJSService(db, session_id)
    response = await svc.get_one_grape_js_project(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


