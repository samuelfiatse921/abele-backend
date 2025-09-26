from typing import Any

import httpx
from fastapi.encoders import jsonable_encoder
from httpx import Timeout
from pydantic import BaseModel

from app.settings import settings
from app.utils.utils import http_exp, logger


class HTTPRequest(BaseModel):
    url: str
    payload: Any = None
    headers: dict = {}
    method: str
    operation: str


async def initiate_http_request(session: str, contact: HTTPRequest):
    headers = contact.headers
    url = contact.url
    method = contact.method.upper()
    operation = contact.operation
    payload = contact.payload

    logger.info(f"{session} - Sending {method} request to {url} to process {operation}. Request body : {payload}")

    response = None
    vendor_response = None

    try:
        async with httpx.AsyncClient(timeout=Timeout(timeout=float(settings.HTTPX_TIMEOUT))) as client:
            if method == "POST":
                response = await client.post(url, headers=headers, json=jsonable_encoder(payload))
            elif method == "GET":
                response = await client.get(url, headers=headers, params=payload)
            elif method == "PUT":
                response = await client.put(url, headers=headers, json=jsonable_encoder(payload))
            elif method == "DELETE":
                response = await client.delete(url, headers=headers)
            response.raise_for_status()  # raise error if not 2xx
    except httpx.ConnectTimeout as e:
        logger.error(f"{session} - Connection timeout occurred : {e}", exc_info=True)
        raise http_exp(500, session=session, exp="Connection timeout")
    except httpx.ReadTimeout as e:
        logger.error(f"{session} - Read timeout occurred : {e}", exc_info=True)
        raise http_exp(500, session=session, exp="Read timeout occurred")
    except httpx.HTTPStatusError as e:
        logger.error(f"{session} - Request failed : {e}", exc_info=True)
        raise http_exp(response.status_code, session=session, exp="Client error occurred")
    except Exception as e:
        logger.error(f"{session} - Exception occurred while initiating request : {e}", exc_info=True)
        raise http_exp(500, session=session, exp="Unknown exception occurred")

    response_content_type = response.headers.get('Content-Type')
    logger.info(f"{session} - Response content type is {response_content_type}")
    content_type_accepted = "application/json" in response_content_type

    if not content_type_accepted:
        raise http_exp(500, session=session, exp="Unexpected response content type received")

    vendor_response = response.json()
    logger.info(f"{session} - Response received is {vendor_response}")

    return vendor_response
