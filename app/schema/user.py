import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, Field

from app.schema.enums import Gender, Status


class CreateUser(BaseModel):
    username: str
    title: str
    firstName: str
    lastName: str
    streetNumber: str
    streetName: str
    email: str
    city: str
    state: str
    country: str
    postcode: str
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    timezoneOffset: Optional[str] = None
    timezoneDescription: Optional[str] = None
    dob: str
    phone: str
    cell: str = "063-9688-877"
    nat: str = "RS"
    gender: Gender
    pictureLarge: str
    pictureMedium: str
    pictureThumbnail: str
    password: str


class GetName(BaseModel):
    title: str
    first: str
    last: str
    username: str


class GetStreet(BaseModel):
    number: str
    name: str


class GetCoordinates(BaseModel):
    longitude: str
    latitude: str


class GetTimezone(BaseModel):
    offset: str
    description: str


class GetLocation(BaseModel):
    street: GetStreet
    city: str
    state: str
    country: str
    postcode: str
    coordinates: GetCoordinates


class GetDate(BaseModel):
    date: str
    age: str


class GetRegistered(BaseModel):
    date: datetime.datetime
    age: str


class GetID(BaseModel):
    name: str = "UUID"
    value: str


class GetPicture(BaseModel):
    large: str
    medium: str
    thumbnail: str


class GetUser(BaseModel):
    gender: Gender
    name: GetName
    location: GetLocation
    email: str
    dob: GetDate
    registered: GetRegistered
    phone: str
    cell: str
    id: GetID
    picture: GetPicture
    nat: str


class FilterUser(BaseModel):
    page: int = 1
    size: int = 20
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    gender: Optional[Gender] = None
    status: Optional[Status] = None


class UpdateUser(BaseModel):
    title: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    username: str
    streetNumber: Optional[str] = None
    streetName: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[str] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    timezoneOffset: Optional[str] = None
    timezoneDescription: Optional[str] = None
    dob: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[Gender] = None
    pictureLarge: Optional[str] = None
    pictureMedium: Optional[str] = None
    pictureThumbnail: Optional[str] = None


class GetUserCredentials(BaseModel):
    userId: uuid.UUID
    username: str
    email: str
    hashed_password: str


class APIResponse(BaseModel):
    code: str = "00"
    message: str = "Success"
    data: list[GetUser] = []
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
    data: list[GetUser] = []
    metadata: Metadata
    systemMessage: str = ""
    systemCode: str = ""
    traceId: str







