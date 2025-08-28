import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.deployment import CreateDeployment, APIResponse, FilterDeployments, APIResponseMetadata, \
    UpdateDeployment
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.repo.deployment import create_deployment, filter_deployment, delete_deployment, update_deployment, \
    get_deployment_by_id
from app.utils.mappers import map_to_deployment, map_to_deployment_list
from app.utils.utils import http_exp, logger


class DeploymentService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create_deployment(self, payload: CreateDeployment) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create deployment : {payload}")

        try:
            new_record = await create_deployment(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Deployment record created")

        return APIResponse(data=[map_to_deployment(new_record)], traceId=self.session)

    async def get_one_deployment(self, deployment_id: uuid.UUID):
        logger.info(f"{self.session} - Handling request to get deployment using id : {deployment_id}")

        deployment = await get_deployment_by_id(self.db, deployment_id)
        if not deployment:
            raise http_exp(status_code=404, session=self.session, code="01", exp="No deployment found")

        logger.info(f"{self.session} - Deployment found")

        result_map = map_to_deployment(deployment)

        return APIResponse(data=[result_map], traceId=self.session)

    async def list_deployments(self, request: FilterDeployments) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering deployment(s) using params : {request}")

        deployments, metadata = await filter_deployment(self.db, request)
        records_found = True if deployments else False

        logger.info(f"{self.session} - Deployment(s) found ? {records_found}")
        mapped_deployment = map_to_deployment_list(deployments) if records_found else []

        return APIResponseMetadata(data=mapped_deployment, metadata=metadata, traceId=self.session)

    async def update_deployment(self, record_id: uuid.UUID, payload: UpdateDeployment) -> APIResponse:
        logger.info(f"{self.session} - Updating deployment {record_id} using payload : {payload}")

        updated_deployment = await update_deployment(self.db, record_id, payload)

        if not updated_deployment:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Deployment not found")

        logger.info(f"{self.session} - Deployment updated")
        return APIResponse(data=[map_to_deployment(updated_deployment)], traceId=self.session)

    async def delete_deployment(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Deleting deployment using record id : {record_id}")

        deleted_deployment = await delete_deployment(self.db, record_id)

        if not deleted_deployment:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Deployment not found")

        logger.info(f"{self.session} - Deployment deleted")
        return APIResponse(data=[map_to_deployment(deleted_deployment)], traceId=self.session)



