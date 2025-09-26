import os
import shutil
import uuid

from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.asset_upload import CreateAsset, FilterAsset, APIResponseMetadata
from app.schema.asset_upload import APIResponse
from app.settings import settings
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.repo.asset_upload import create_asset, filter_assets, delete_asset
from app.utils.mappers import map_to_uploaded_asset, map_to_uploaded_asset_list
from app.utils.utils import http_exp, logger


class AssetUploadService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create_asset(self, file: UploadFile, user_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create asset : {file}")

        try:
            # Validate extension
            ext = file.filename.split(".")[-1].lower()
            if ext not in set(settings.ALLOWED_EXTENSIONS.split(",")):
                raise HTTPException(status_code=400, detail=f"File type .{ext} not allowed")

            # Validate file size (read first then reset pointer)
            file.file.seek(0, os.SEEK_END)  # move to end
            file_size = file.file.tell()  # get position == size in bytes
            file.file.seek(0)  # reset pointer

            max_bytes = int(settings.MAX_FILE_SIZE_MB) * 1024 * 1024
            if file_size > max_bytes:
                raise HTTPException(status_code=400, detail=f"File too large. Max {file_size}MB allowed")

            from app.main import upload_folder

            # Save file to folder
            file_location = os.path.join(upload_folder, file.filename)
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            asset = CreateAsset(userId=user_id, fileName=file.filename, filePath=file_location)

            new_record = await create_asset(self.db, asset)
        except DatabaseException as exp:
            logger.error("error uploading", exc_info=True)
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            logger.error("error uploading", exc_info=True)

            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Asset created")

        return APIResponse(data=[map_to_uploaded_asset(new_record)], traceId=self.session)

    async def list_asset(self, request: FilterAsset) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering asset(s) using params : {request}")

        assets, metadata = await filter_assets(self.db, request)
        records_found = True if assets else False

        logger.info(f"{self.session} - Asset(s) found ? {records_found}")
        mapped_asset = map_to_uploaded_asset_list(assets) if records_found else []

        return APIResponseMetadata(data=mapped_asset, metadata=metadata, traceId=self.session)

    async def delete_asset(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Deleting asset using record id : {record_id}")

        deleted_asset = await delete_asset(self.db, record_id)

        if not deleted_asset:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Asset not found")

        logger.info(f"{self.session} - Asset deleted")
        return APIResponse(data=[map_to_uploaded_asset(deleted_asset)], traceId=self.session)





