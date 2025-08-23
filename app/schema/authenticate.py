import uuid

from pydantic import BaseModel


class GetAuthentication(BaseModel):
    userId: uuid.UUID
    accessToken: str
    refreshToken: str
    tokenType: str = "bearer"


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetAuthentication]
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str




