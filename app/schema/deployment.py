import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class CreateDeployment(BaseModel):
    name: str
    deploymentSupportCost: float
    deploymentSupportDescription: str
    domainSupportCost: float
    domainSupportDescription: str


class GetDeployment(CreateDeployment):
    id: uuid.UUID
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class UpdateDeployment(BaseModel):
    name: Optional[str] = None
    deploymentSupportCost: Optional[float] = None
    deploymentSupportDescription: Optional[str] = None
    domainSupportCost: Optional[float] = None
    domainSupportDescription: Optional[str] = None


class FilterDeployments(BaseModel):
    page: int = 1
    size: int = 20
    name: Optional[str] = None


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetDeployment] = []
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
    data: list[GetDeployment] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str



