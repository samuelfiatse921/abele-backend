from pydantic import BaseModel


class APIResponseFailure(BaseModel):
    code: str
    msg: str
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str

