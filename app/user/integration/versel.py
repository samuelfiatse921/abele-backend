from app.schema.versel import CreateVercelDeployment, VercelDeploymentResponse
from app.settings import settings
from app.utils.http_client import HTTPRequest, initiate_http_request


async def deploy_project(session: str, payload: CreateVercelDeployment) -> str:
    request = HTTPRequest(
        headers={
            "Authorization": f"Bearer {settings.VERCEL_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST",
        operation="deploy_project",
        url=f"{settings.VERCEL_API}?skipAutoDetectionConfirmation=1",
        payload=payload,
    )

    vendor_response = await initiate_http_request(session, request)
    deployment_result = VercelDeploymentResponse(**vendor_response)

    return deployment_result.name
