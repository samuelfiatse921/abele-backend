import datetime
import uuid

from pydantic import BaseModel, Field


class CreateProject(BaseModel):
    userId: uuid.UUID
    templateId: uuid.UUID
    data: list


class GetProject(BaseModel):
    id: uuid.UUID
    userId: uuid.UUID
    templateId: uuid.UUID
    data: list
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class UpdateProject(BaseModel):
    data: list


class FilterProject(BaseModel):
    user_id: uuid.UUID
    template_id: uuid.UUID


class DeleteProject(BaseModel):
    user_id: uuid.UUID
    template_id: uuid.UUID


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetProject] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class Metadata(BaseModel):
    seed: str = Field(default_factory=lambda: str(uuid.uuid4()))
    results: int
    page: int
    totalPages: int
    version: str = "1.0"

