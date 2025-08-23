import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.wallet import APIResponse, FilterWallet, APIResponseMetadata, CreditWallet
from app.user.services.wallet import WalletService
from app.utils.utils import generate_uuid_str, logger

wallet_router = APIRouter()


@wallet_router.post("/credit")
async def credit_wallet(
    payload: CreditWallet,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to credit wallet using payload : {payload}")

    wallet_svc = WalletService(db, session_id)
    response = await wallet_svc.credit_wallet(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@wallet_router.get("/single/{record_id}")
async def get_single_wallet(
    record_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to get a single wallet using id : {record_id}")

    wallet_svc = WalletService(db, session_id)
    response = await wallet_svc.get_one_wallet(record_id)

    logger.info(f"{session_id} - Response : {response}")

    return response


@wallet_router.get("/list")
async def list_wallet(
    filter_query: Annotated[FilterWallet, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Filtering wallet(s) using payload : {filter_query}")

    wallet_svc = WalletService(db, session_id)
    response = await wallet_svc.list_wallets(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response




