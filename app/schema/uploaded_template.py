import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from app.schema.enums import TemplateCategory, TemplateTier, TemplateUnder


class TemplateFiles(BaseModel):
    htmlFiles: list[str]
    cssFiles: list[str]
    jsFiles: list[str]


class CreateUploadedTemplate(BaseModel):
    image: str
    name: str
    ownerId: uuid.UUID
    price: float
    coin: int
    liveDemo: str
    tier: TemplateTier
    category: TemplateCategory
    under: TemplateUnder
    files: TemplateFiles


class BaseUploadedTemplate(BaseModel):
    id: uuid.UUID
    image: str
    templateName: str
    price: float
    coin: int
    tier: TemplateTier
    liveDemo: str
    category: TemplateCategory
    under: TemplateUnder
    templateFiles: TemplateFiles
    reviews: int
    rating: int
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class GetUploadedTemplate(BaseUploadedTemplate):
    ownerId: uuid.UUID


class GetJoinedUploadedUserTemplate(BaseUploadedTemplate):
    owner: str
    template: str


class UpdateUploadedTemplate(BaseModel):
    image_path: Optional[str] = None
    price: Optional[float] = None
    type: Optional[TemplateTier] = None
    liveDemo: Optional[str] = None
    category: Optional[TemplateCategory] = None
    htmlFiles: Optional[list[str]] = None
    cssFiles: Optional[list[str]] = None
    jsFiles: Optional[list[str]] = None


class FilterUploadedTemplate(BaseModel):
    page: int = 1
    size: int = 20
    ownerId: Optional[uuid.UUID] = None
    tier: Optional[TemplateTier] = None
    category: Optional[TemplateCategory] = None
    under: Optional[TemplateUnder] = None


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetUploadedTemplate] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class SingleRecordAPIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetJoinedUploadedUserTemplate] = []
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
    data: list[GetJoinedUploadedUserTemplate] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str




