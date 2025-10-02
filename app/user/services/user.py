import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import session_maker
from app.schema.asset_upload import CreateAsset
from app.schema.braintree import Customer
from app.schema.user import CreateUser, APIResponse, FilterUser, APIResponseMetadata, UpdateUser, GetUserCredentials
from app.schema.wallet import CreateWallet
from app.settings import settings
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.integration.braintree import create_customer
from app.user.models.user import User
from app.user.repo.asset_upload import create_asset
from app.utils.mappers import map_to_user, map_to_user_list, map_to_user_credentials
from app.user.repo.user import create_user, get_user_by_id, filter_users, update_user_by_id, get_user_by_phone_number, \
    get_user_by_email, get_user_by_username
from app.user.services.wallet import WalletService
from app.utils.utils import http_exp, logger


class UserService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def create(self, payload: CreateUser) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create user : {payload}")

        await self.__check_unique_fields_exist(payload)

        try:
            new_user = await create_user(self.db, payload)
            asyncio.create_task(self.create_wallet(new_user))
            asyncio.create_task(self.create_default_assets(new_user))
            asyncio.create_task(self.create_braintree_customer(new_user))
        except DatabaseException as exp:
            raise http_exp(500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - New user created")

        return APIResponse(data=[map_to_user(new_user)], traceId=self.session)

    async def create_default_assets(self, new_user):
        async with session_maker() as db:
            default_assets = settings.DEFAULT_IMAGES_LIST
            for default_asset in default_assets:
                asset = CreateAsset(
                    userId=new_user.id, fileName=default_asset.get("fileName"), filePath=default_asset.get("filePath")
                )
                await create_asset(db, asset)

    async def create_wallet(self, new_user):
        async with session_maker() as db:
            wallet_svc = WalletService(db, self.session)
            await wallet_svc.create_wallet(CreateWallet(userId=new_user.id))

    async def create_braintree_customer(self, new_user: User):
        customer = Customer(
            id=str(new_user.id),
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            phone=new_user.phone,
            email=new_user.email
        )
        await create_customer(self.session, customer)

    async def get_one_user(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Handling request to get user using id : {record_id}")

        user = await get_user_by_id(self.db, record_id)

        if not user:
            raise http_exp(404, code="01", session=self.session, msg="No user found")

        logger.info(f"{self.session} - User found")

        return APIResponse(data=[map_to_user(user)], traceId=self.session)

    async def list_users(self, payload: FilterUser) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering user(s) using params : {payload}")

        users, metadata = await filter_users(self.db, payload)
        users_found = True if users and len(users) > 0 else False

        logger.info(f"{self.session} - User(s) found ? {users_found}")
        mapped_users = map_to_user_list(users) if users_found else []

        return APIResponseMetadata(data=mapped_users, metadata=metadata, traceId=self.session)

    async def update_user(
        self,
        record_id: uuid.UUID,
        payload: UpdateUser
    ) -> APIResponse:
        logger.info(f"{self.session} - Updating user {record_id} using payload : {payload}")

        updated_user = await update_user_by_id(self.db, record_id, payload)

        if not updated_user:
            raise http_exp(status_code=404, session=self.session, code="01", msg="User not found")

        logger.info(f"{self.session} - User updated")
        return APIResponse(data=[map_to_user(updated_user)], traceId=self.session)

    async def get_user_credential(self, username: str) -> GetUserCredentials:
        user = await get_user_by_username(self.db, username=username)
        return map_to_user_credentials(user) if user else None

    async def check_username_exist(self, username: str):
        result = await self.list_users(payload=FilterUser(username=username))
        if len(result.data) > 0:
            raise http_exp(status_code=400, session=self.session, code="01", msg="Username already exist")

    async def check_phone_number_exist(self, phone_number: str):
        if await get_user_by_phone_number(db=self.db, phone_number=phone_number):
            raise http_exp(status_code=400, session=self.session, code="01", msg="Phone number already exist")

    async def check_email_exist(self, email: str):
        if await get_user_by_email(db=self.db, email=email):
            raise http_exp(status_code=400, session=self.session, code="01", msg="Email already exist")

    async def __check_unique_fields_exist(self, payload: CreateUser):
        await self.check_email_exist(payload.email)
        await self.check_username_exist(payload.username)
        await self.check_phone_number_exist(payload.phone)


