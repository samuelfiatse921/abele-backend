import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import get_db_session
from app.schema.following import CreateFollowing, APIResponse, FilterFollowings, FilterFollowers
from app.schema.user import APIResponseMetadata
from app.user.services.following import FollowingService
from app.utils.utils import generate_uuid_str, logger

following_router = APIRouter()


@following_router.post("")
async def create_following(
    payload: CreateFollowing,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received to create new user follower : {payload}")

    following_svc = FollowingService(db, session_id)
    response = await following_svc.create_following(payload)

    logger.info(f"{session_id} - Response : {response}")

    return response


@following_router.get("/list/by-user/")
async def list_user_followings(
    filter_query: Annotated[FilterFollowings, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Request received to list user followings : {filter_query}")

    following_svc = FollowingService(db, session_id)
    response = await following_svc.list_followings(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@following_router.get("/list/for-user")
async def list_user_followers(
    filter_query: Annotated[FilterFollowers, Query()],
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponseMetadata:
    logger.info(f"{session_id} - Request received to list users following user : {filter_query}")

    following_svc = FollowingService(db, session_id)
    response = await following_svc.list_followers(filter_query)

    logger.info(f"{session_id} - Response : {response}")

    return response


@following_router.delete("/{user_id}/unfollow/{following_id}")
async def unfollower_user(
    user_id: uuid.UUID,
    following_id: uuid.UUID,
    session_id: str = Depends(generate_uuid_str),
    db: AsyncSession = Depends(get_db_session)
) -> APIResponse:
    logger.info(f"{session_id} - Request received from user {user_id} to unfollower user using following id : {following_id}")

    following_svc = FollowingService(db, session_id)
    response = await following_svc.unfollower_user(following_id)

    logger.info(f"{session_id} - Response : {response}")

    return response



