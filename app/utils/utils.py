import logging
import uuid
from datetime import date, datetime
from typing import Optional

import pycountry
from fastapi import HTTPException
from sqlalchemy import desc, select

from app.schema.http import APIResponseFailure


logger = logging.getLogger("SizeMugBackend")


def build_base_query(model):
    return select(model).order_by(desc(model.created_on)).limit(1)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def generate_uuid_str() -> str:
    return str(generate_uuid())


def http_exp(
    status_code: int,
    session: str,
    code: Optional[str] = "02",
    msg: Optional[str] = "Request failed",
    exp: Optional[str] = "N/A"
):
    return HTTPException(
        status_code=status_code,
        detail=APIResponseFailure(code=code, msg=msg, traceId=session, systemMessage=exp).model_dump()
    )


def get_age(birthdate_str: str, fmt: str = "%d/%m/%Y") -> int:
    # Convert string to date
    birthdate = datetime.strptime(birthdate_str, fmt).date()
    today = date.today()

    # Calculate age
    age = today.year - birthdate.year - (
            (today.month, today.day) < (birthdate.month, birthdate.day)
    )
    return age


def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        if country:
            return country.alpha_2
        # Sometimes names are not exact matches, try lookup
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2 # type: ignore[attr-defined]
    except LookupError:
        return country_name

