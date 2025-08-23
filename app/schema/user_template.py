import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CreateUserTemplate(BaseModel):
    templateId: uuid.UUID
    userId: uuid.UUID


class GetUserTemplate(BaseModel):
    id: uuid.UUID
    templateId: uuid.UUID
    userId: uuid.UUID
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class FilterUserTemplate(BaseModel):
    page: int = 1
    size: int = 20
    userId: uuid.UUID
    templateId: Optional[uuid.UUID] = None
    paymentId: Optional[uuid.UUID] = None


class Metadata(BaseModel):
    seed: str = Field(default_factory=lambda: str(uuid.uuid4()))
    results: int
    page: int
    totalPages: int
    version: str = "1.0"


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetUserTemplate] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str

