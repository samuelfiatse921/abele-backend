import base64

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.grapejs_project import FilterProject
from app.schema.versel import DeploySingleFile, DeployEntireProject, VercelProject, \
    CreateVercelDeployment, APIResponse
from app.user.integration.versel import deploy_project
from app.user.services.grapejs_project import GrapeJSService
from app.utils.utils import logger, generate_uuid


class VercelService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session
        self.grape_js_svc = GrapeJSService(self.db, self.session)
        self.template_format = """
            <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8" />
                <title>[[templateTitle]]</title>
                <style>[[templateStyles]]</style>
              </head>
              [[templateBody]]
            </html>
        """

    async def deploy_single_file(self, request: DeploySingleFile) -> APIResponse:
        logger.info(f"{self.session} - Handling request to deploy single file : {request}")

        filter_project = FilterProject(user_id=request.userId, template_id=request.templateId, page=request.page)
        record = await self.grape_js_svc.get_one_grape_js_project(filter_project)
        project_details = record.data[0].data
        logger.info(f"logged project details {project_details}")
        project = next(
            (rec for rec in project_details if rec["id"] == request.page), None  # default if not found
        )

        logger.info(f"{self.session} - Single page found : {project}")
        page_name = project["name"]
        template = self.build_template(page_name, project)

        logger.info("Preparing project deployment")
        vercel_project = self.build_versel_project(page_name, template)

        project_id = str(generate_uuid())
        template_name = project_id[0:len(project_id)-1]
        deployment_url = await self.run_deployment(template_name, [vercel_project])

        full_deployment_url = f"{deployment_url}/{vercel_project.file}"
        return APIResponse(data=[full_deployment_url], traceId=self.session)

    async def deploy_entire_project(self, request: DeployEntireProject):
        logger.info(f"{self.session} - Handling request to deploy entire project : {request}")

        filter_project = FilterProject(user_id=request.userId, template_id=request.templateId)
        record = await self.grape_js_svc.get_one_grape_js_project(filter_project)

        logger.info(f"{self.session} - Project found. Preparing project deployment")
        project_details = record.data[0].data

        files: list[VercelProject] = []

        for project in project_details:
            project_name = project["name"]
            if project_name:
                page_name = project_name
                template = self.build_template(page_name, project)
                vercel_project = self.build_versel_project(page_name, template)
                files.append(vercel_project)

        project_id = str(generate_uuid())
        template_name = project_id[0:len(project_id) - 1]
        deployment_url = await self.run_deployment(template_name, files)

        return APIResponse(data=[deployment_url], traceId=self.session)

    async def run_deployment(self, template_name, vercel_project):
        deployment_payload = CreateVercelDeployment(name=template_name, files=vercel_project)
        logger.info(f"{self.session} - About to deploy project using payload : {deployment_payload}")

        deployment_details = await deploy_project(self.session, deployment_payload)
        deployment_url = f"https://{deployment_details}.vercel.app"
        logger.info(f"{self.session} - Project deployed successfully on {deployment_url}")

        return deployment_url

    def build_template(self, page_name, project_details):
        css_page = project_details["cssPage"]
        html_page = project_details["htmlPage"]

        template = (
            self.template_format
            .replace("[[templateTitle]]", page_name)
            .replace("[[templateStyles]]", css_page)
            .replace("[[templateBody]]", html_page)
        )

        logger.info(f"{self.session} - Template built for {page_name} : {template}")

        return template

    def build_versel_project(self, page_name, template):
        encoded_page = base64.b64encode(template.encode()).decode()
        vercel_project = VercelProject(file=f"{page_name}.html", data=encoded_page)
        return vercel_project


