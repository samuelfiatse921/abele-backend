from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.versel import APIResponse, DeployEntireProject, DeploySingleFile
from app.user.services.versel import VercelService
from app.utils.utils import generate_uuid_str, logger

vercel_router = APIRouter()


@vercel_router.post("/single-file")
async def deploy_single_file(
    payload: DeploySingleFile,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
) -> APIResponse:
    logger.info(f"{session_id} - Request received to deploy single file : {payload}")

    vercel_svc = VercelService(db, session_id)
    response = await vercel_svc.deploy_single_file(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@vercel_router.post("/entire-project")
async def deploy_entire_project(
    payload: DeployEntireProject,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
) -> APIResponse:
    logger.info(f"{session_id} - Request received to deploy entire project : {payload}")

    vercel_svc = VercelService(db, session_id)
    response = await vercel_svc.deploy_entire_project(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response

