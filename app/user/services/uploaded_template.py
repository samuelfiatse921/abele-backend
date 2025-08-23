import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.uploaded_template import CreateUploadedTemplate, APIResponse, APIResponseMetadata, \
    FilterUploadedTemplate, UpdateUploadedTemplate, SingleRecordAPIResponse
from app.user.exceptions.custom_exceptions import DatabaseException
from app.utils.mappers import map_to_joined_uploaded_template_and_user, map_to_joined_uploaded_template_and_user_list, \
    map_to_uploaded_template
from app.user.repo.uploaded_template import create_uploaded_template, get_joined_uploaded_template_and_user_by_id, \
    filter_uploaded_template, update_uploaded_template_by_id, delete_uploaded_template_by_id
from app.user.services.user import UserService
from app.utils.utils import http_exp, logger


class TemplateUploadService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create_uploaded_template(self, payload: CreateUploadedTemplate) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create uploaded template : {payload}")

        user_svc = UserService(self.db, self.session)
        await user_svc.get_one_user(payload.ownerId)
        logger.info(f"{self.session} - User record found")

        try:
            new_uploaded_template = await create_uploaded_template(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Uploaded template record created")

        return APIResponse(data=[map_to_uploaded_template(new_uploaded_template)], traceId=self.session)

    async def get_one_uploaded_template(self, record_id: uuid.UUID) -> SingleRecordAPIResponse:
        logger.info(f"{self.session} - Handling request to get uploaded template using id : {record_id}")

        result = await get_joined_uploaded_template_and_user_by_id(self.db, record_id)
        if not result:
            raise http_exp(status_code=404, session=self.session, code="01", exp="No uploaded template found")

        uploaded_template, user = result[0].tuple()

        logger.info(f"{self.session} - Uploaded template found")

        return SingleRecordAPIResponse(data=[map_to_joined_uploaded_template_and_user(uploaded_template, user)], traceId=self.session)

    async def list_uploaded_templates(self, request: FilterUploadedTemplate) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering uploaded template(s) using params : {request}")

        uploaded_templates, metadata = await filter_uploaded_template(self.db, request)
        wallets_found = True if uploaded_templates and len(uploaded_templates) > 0 else False

        logger.info(f"{self.session} - Uploaded template(s) found ? {wallets_found}")
        mapped_wallets = map_to_joined_uploaded_template_and_user_list(uploaded_templates) if wallets_found else []

        return APIResponseMetadata(data=mapped_wallets, metadata=metadata, traceId=self.session)

    async def update_uploaded_template(
        self,
        record_id: uuid.UUID,
        payload: UpdateUploadedTemplate
    ) -> APIResponse:
        logger.info(f"{self.session} - Updating uploaded template {record_id} using payload : {payload}")

        updated_template = await update_uploaded_template_by_id(self.db, record_id, payload)

        if not updated_template:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Uploaded template not found")

        logger.info(f"{self.session} - Uploaded template updated")
        return APIResponse(data=[map_to_uploaded_template(updated_template)], traceId=self.session)

    async def delete_uploaded_template(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Deleting uploaded template using id : {record_id}")

        deleted_template = await delete_uploaded_template_by_id(self.db, record_id)

        if not deleted_template:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Uploaded template not found")

        logger.info(f"{self.session} - Uploaded template deleted")
        return APIResponse(data=[map_to_uploaded_template(deleted_template)], traceId=self.session)




