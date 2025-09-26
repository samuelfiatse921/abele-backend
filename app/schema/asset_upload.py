import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CreateAsset(BaseModel):
    userId: uuid.UUID
    fileName: str
    filePath: str


class GetAsset(BaseModel):
    id: uuid.UUID
    fileName: str
    filePath: str
    createdOn: datetime.datetime


class FilterAsset(BaseModel):
    page: int = 1
    size: int = 20
    asset_name: Optional[str] = None
    user_id: uuid.UUID


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetAsset] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class Metadata(BaseModel):
    seed: str = Field(default_factory=lambda: str(uuid.uuid4()))
    results: int
    page: int
    totalPages: int
    version: str = "1.0"


class APIResponseMetadata(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetAsset] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str
