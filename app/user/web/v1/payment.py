import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.deps.db.db import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.services.payment import PaymentService
from app.schema.payment import APIResponse, APIResponseMetadata, FilterPayment, GenerateTokenAPIResponse
from app.utils.utils import generate_uuid_str, logger

payment_router = APIRouter()


@payment_router.get("/generate/token/{user_id}")
async def generate_client_token(
    user_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> GenerateTokenAPIResponse:
    logger.info(f"{session_id} - Request received to generate payment token for user : {user_id}")

    payment_service = PaymentService(db, session_id)
    response = await payment_service.generate_client_token(user_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@payment_router.get("/single/{payment_id}")
async def get_single_payment(
    payment_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to get a payment using id : {payment_id}")

    payment_service = PaymentService(db, session_id)
    response = await payment_service.get_one_payment(payment_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@payment_router.get("/list")
async def list_payments(
    filter_query: Annotated[FilterPayment, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering payment(s) using payload : {filter_query}")

    payment_service = PaymentService(db, session_id)
    response = await payment_service.list_payments(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


