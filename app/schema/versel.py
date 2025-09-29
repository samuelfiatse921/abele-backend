import uuid
from typing import Optional

from pydantic import BaseModel


class DeploySingleFile(BaseModel):
    templateName: str
    templateId: uuid.UUID
    userId: uuid.UUID
    page: str


class DeployEntireProject(BaseModel):
    templateName: str
    templateId: uuid.UUID
    userId: uuid.UUID


class VercelProject(BaseModel):
    file: str
    data: str
    encoding: str = "base64"


class ProjectSettings(BaseModel):
    framework: Optional[str] = None


class CreateVercelDeployment(BaseModel):
    name: str
    files: list[VercelProject]
    public: bool = True
    projectSettings: ProjectSettings = ProjectSettings()


class VercelDeploymentResponse(BaseModel):
    name: str

    class Config:
        extra = "ignore"


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[str] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str

