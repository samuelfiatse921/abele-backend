import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.deps.db.db import session_maker
from app.schema.enums import TemplateTier
from app.schema.uploaded_template import APIResponseMetadata
from app.schema.user_template import CreateUserTemplate, APIResponse, FilterUserTemplate
from app.schema.wallet import FilterWallet
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.services.deployment import DeploymentService
from app.utils.mappers import map_to_user_template, map_to_joined_uploaded_user_template_list
from app.user.repo.user_template import create_user_template, filter_user_template, delete_user_template
from app.user.services.uploaded_template import TemplateUploadService
from app.user.services.user import UserService
from app.user.services.wallet import WalletService
from app.utils.utils import http_exp, logger


class UserTemplateService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session
        self.user_svc = UserService(self.db, self.session)
        self.wallet_svc = WalletService(self.db, self.session)
        self.uploaded_template_svc = TemplateUploadService(self.db, self.session)

    async def create_user_template(self, payload: CreateUserTemplate):
        logger.info(f"{self.session} - Handling request to create user template : {payload}")

        user_id = payload.userId
        logger.info(f"{self.session} - Getting user details using id : {user_id}")

        await self.user_svc.get_one_user(user_id)
        logger.info(f"{self.session} - User record found")

        template_cost = await self.__check_template_access_eligibility(user_id, payload.templateId, payload.deploymentId)
        logger.info(f"{self.session} - User passed eligibility check. Creating user template")

        try:
            new_user_template = await create_user_template(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - User template record created")

        asyncio.create_task(self.debit_user_wallet(user_id, payload.deploymentId, template_cost))

        return APIResponse(data=[map_to_user_template(new_user_template)], traceId=self.session)

    async def debit_user_wallet(self, user_id: uuid.UUID, deployment_id: uuid.UUID, amount: float):
        async with session_maker() as db:
            total_cost = await self.compute_deployment_cost(db, deployment_id)
            amount += total_cost
            wallet_svc = WalletService(db, self.session)
            await wallet_svc.debit_wallet(user_id=user_id, amount=amount)

    async def compute_deployment_cost(self, db, deployment_id):
        deployment_svc = DeploymentService(db, self.session)
        deployment_result = await deployment_svc.get_one_deployment(deployment_id)

        deployment_data = deployment_result.data[0]
        deployment_cost = deployment_data.deploymentSupportCost

        domain_cost = deployment_data.domainSupportCost
        return deployment_cost + domain_cost

    async def __check_template_access_eligibility(
        self,
        user_id: uuid.UUID,
        template_id: uuid.UUID,
        deployment_id: uuid.UUID
    ) -> float:
        logger.info(f"{self.session} - Getting wallet details using user id : {user_id}")
        wallet_details = await self.wallet_svc.list_wallets(request=FilterWallet(userId=user_id))

        wallet_found = len(wallet_details.data) > 0
        logger.info(f"{self.session} - Wallet found ? {wallet_found}")

        if not wallet_found:
            raise http_exp(404, code="01", session=self.session, msg="No wallet found for user")

        logger.info(f"{self.session} - Getting template details using template id : {template_id}")
        template_details = await self.uploaded_template_svc.get_one_uploaded_template(template_id)
        template_found = template_details is not None
        logger.info(f"{self.session} - Template found ? {template_found}")

        if not template_found:
            raise http_exp(404, code="01", session=self.session, msg="No template found")

        template_cost = template_details.data[0].price
        wallet_balance = wallet_details.data[0].balance
        total_deployment_cost = await self.compute_deployment_cost(self.db, deployment_id)

        is_template_free = template_details.data[0].tier == TemplateTier.FREE
        logger.info(f"{self.session} - Is template free ? {is_template_free}")

        total_debit_amount = total_deployment_cost + template_cost
        logger.info(f"{self.session} - Total amount to debit(template cost + deployment cost) is {total_debit_amount}")

        user_has_enough_balance = is_template_free or (wallet_balance - total_debit_amount) >= 0
        logger.info(f"{self.session} - Does user have enough funds in wallet ? {user_has_enough_balance}")

        if not user_has_enough_balance:
            raise http_exp(400, code="01", session=self.session, msg="Wallet doesn't have enough funds")

        return template_cost

    async def list_user_templates(self, payload: FilterUserTemplate) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering user(s) using params : {payload}")

        templates, metadata = await filter_user_template(self.db, payload)
        templates_found = True if templates and len(templates) > 0 else False

        logger.info(f"{self.session} - User template(s) found ? {templates_found}")
        mapped_uploaded_templates = map_to_joined_uploaded_user_template_list(templates) if templates_found else []

        return APIResponseMetadata(data=mapped_uploaded_templates, metadata=metadata, traceId=self.session)

    async def delete_user_template(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Deleting template using id : {record_id}")

        deleted_template = await delete_user_template(self.db, record_id)

        if not deleted_template:
            raise http_exp(status_code=404, session=self.session, code="01", msg="User template not found")

        logger.info(f"{self.session} - User template deleted")
        return APIResponse(data=[map_to_user_template(deleted_template)], traceId=self.session)

