import uuid
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.asset_upload import FilterAsset, APIResponseMetadata, APIResponse
from app.user.services.asset_upload import AssetUploadService
from app.utils.utils import logger, generate_uuid_str

asset_upload_router = APIRouter()


@asset_upload_router.post("/upload/{user_id}")
async def upload_file(
    user_id: uuid.UUID,
    file: UploadFile = File(...),
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Handling request to create asset : {file}")

    svc = AssetUploadService(db, session_id)
    response = await svc.create_asset(file, user_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@asset_upload_router.get("/list")
async def list_uploaded_assets(
    filter_query: Annotated[FilterAsset, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering uploaded asset(s) using payload : {filter_query}")

    svc = AssetUploadService(db, session_id)
    response = await svc.list_asset(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@asset_upload_router.delete("/{record_id}/from-user/{user_id}")
async def delete_asset(
    record_id: uuid.UUID,
    user_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session),
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to delete asset : {record_id}")

    svc = AssetUploadService(db, session_id)
    response = await svc.delete_asset(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response



