import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from app.schema.enums import Status


class CreateWallet(BaseModel):
    userId: uuid.UUID
    balance: float = 0


class GetWallet(BaseModel):
    id: uuid.UUID
    userId: uuid.UUID
    balance: float
    createdOn: datetime.datetime
    updatedOn: datetime.datetime


class DeviceData(BaseModel):
    correlation_id: str


class CreditWallet(BaseModel):
    amount: float
    user_id: str
    payment_nonce: str
    device_data: DeviceData


class DebitWallet(BaseModel):
    amount: float


class UpdateWalletStatus(BaseModel):
    status: Optional[Status] = None


class FilterWallet(BaseModel):
    page: int = 1
    size: int = 20
    userId: Optional[uuid.UUID] = None
    status: Optional[Status] = None


class Metadata(BaseModel):
    seed: str = Field(default_factory=lambda: str(uuid.uuid4()))
    results: int
    page: int
    totalPages: int
    version: str = "1.0"


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetWallet]
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class APIResponseMetadata(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetWallet] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str



