import datetime
import uuid

from pydantic import BaseModel, Field


class CreateProject(BaseModel):
    id: uuid.UUID
    data: dict


class GetProject(BaseModel):
    id: uuid.UUID
    data: dict
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class UpdateProject(BaseModel):
    data: dict


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

