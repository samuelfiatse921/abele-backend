import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schema.enums import PaymentStatus


class CreatePayment(BaseModel):
    amount: float
    user_id: str
    narration: str = "top up wallet"
    paymentNonce: str


class GetPayment(BaseModel):
    id: uuid.UUID
    currency: str
    amount: float
    reference: uuid.UUID
    external_reference: str
    userId: uuid.UUID
    processorId: str
    narration: str
    status: PaymentStatus
    createdOn: datetime
    updatedOn: datetime


class UpdatePaymentStatus(BaseModel):
    status: Optional[PaymentStatus] = None
    externalReference: Optional[str] = None


class FilterPayment(BaseModel):
    page: int = 1
    size: int = 20
    reference: Optional[uuid.UUID] = None
    user_id: Optional[uuid.UUID] = None
    payment_nonce: Optional[str] = None
    status: Optional[PaymentStatus] = None


class GenerateTokenAPIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[str]
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class Metadata(BaseModel):
    seed: str = Field(default_factory=lambda: str(uuid.uuid4()))
    results: int
    page: int
    totalPages: int
    version: str = "1.0"


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetPayment] = []
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str


class APIResponseMetadata(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetPayment] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str

