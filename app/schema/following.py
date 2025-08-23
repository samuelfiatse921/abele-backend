import datetime
import uuid

from pydantic import BaseModel, Field


class CreateFollowing(BaseModel):
    userId: uuid.UUID
    followingUserId: uuid.UUID


class GetFollowing(BaseModel):
    id: uuid.UUID
    userId: uuid.UUID
    followingUserId: uuid.UUID
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class FilterFollowings(BaseModel):
    page: int = 1
    size: int = 20
    userId: uuid.UUID


class FilterFollowers(BaseModel):
    page: int = 1
    size: int = 20
    userId: uuid.UUID


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetFollowing] = []
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
    data: list[GetFollowing] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str
