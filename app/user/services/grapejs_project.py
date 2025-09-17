import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.grapejs_project import CreateProject, APIResponse, FilterProject, DeleteProject
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.repo.grapejs_project import create_or_update_project, get_project_by_id, delete_project
from app.utils.mappers import map_to_grape_js_project
from app.utils.utils import http_exp, logger


class GrapeJSService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create_grape_js_project(self, payload: CreateProject) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create grape-js project : {payload}")

        try:
            new_record = await create_or_update_project(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - GrapeJS project record created")

        return APIResponse(data=[map_to_grape_js_project(new_record)], traceId=self.session)

    async def get_one_grape_js_project(self, request: FilterProject) -> APIResponse:
        logger.info(f"{self.session} - Handling request to get grape-js project using filter : {request}")

        project = await get_project_by_id(self.db, request)
        if not project:
            raise http_exp(status_code=404, session=self.session, code="01", exp="No project found")

        logger.info(f"{self.session} - Project found")

        return APIResponse(data=[map_to_grape_js_project(project)], traceId=self.session)

    async def delete_grape_js_project(self, request: DeleteProject) -> APIResponse:
        logger.info(f"{self.session} - Deleting project using request : {request}")

        deleted_project = await delete_project(self.db, request)

        if not deleted_project:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Project not found")

        logger.info(f"{self.session} - Project deleted")
        return APIResponse(data=[map_to_grape_js_project(deleted_project)], traceId=self.session)


