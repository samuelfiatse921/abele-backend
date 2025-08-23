import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.following import CreateFollowing, APIResponse, FilterFollowings, FilterFollowers
from app.schema.user import APIResponseMetadata
from app.user.exceptions.custom_exceptions import DatabaseException
from app.utils.mappers import map_to_following, map_to_user_list
from app.user.repo.following import create_following, filter_followings, filter_followers, \
    unfollower_user_by_id
from app.utils.utils import http_exp, logger


class FollowingService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create_following(self, payload: CreateFollowing) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create following : {payload}")

        try:
            new_record = await create_following(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Following record created")

        return APIResponse(data=[map_to_following(new_record)], traceId=self.session)

    async def list_followings(self, request: FilterFollowings) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering followings(s) using params : {request}")

        followings, metadata = await filter_followings(self.db, request)
        records_found = True if followings and len(followings) > 0 else False

        logger.info(f"{self.session} - Following(s) found ? {records_found}")
        mapped_followings = map_to_user_list(followings) if records_found else []

        return APIResponseMetadata(data=mapped_followings, metadata=metadata, traceId=self.session)

    async def list_followers(self, request: FilterFollowers) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering follower(s) using params : {request}")

        followers, metadata = await filter_followers(self.db, request)
        records_found = True if followers and len(followers) > 0 else False

        logger.info(f"{self.session} - Follower(s) found ? {records_found}")
        mapped_followings = map_to_user_list(followers) if records_found else []

        return APIResponseMetadata(data=mapped_followings, metadata=metadata, traceId=self.session)

    async def unfollower_user(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Unfollower user using following record id : {record_id}")

        deleted_follower = await unfollower_user_by_id(self.db, record_id)

        if not deleted_follower:
            raise http_exp(status_code=404, session=self.session, code="01", msg="Follower not found")

        logger.info(f"{self.session} - User unfollowed")
        return APIResponse(data=[map_to_following(deleted_follower)], traceId=self.session)



