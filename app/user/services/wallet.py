import asyncio
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.payment import CreatePayment, UpdatePaymentStatus
from app.schema.wallet import CreateWallet, APIResponse, FilterWallet, APIResponseMetadata, CreditWallet, DebitWallet
from app.schema.enums import PaymentStatus
from app.user.exceptions.custom_exceptions import DatabaseException
from app.utils.mappers import map_to_wallet, map_to_wallet_list
from app.user.repo.wallet import create_wallet, get_wallet_by_id, filter_wallets, credit_wallet, debit_wallet
from app.user.services.payment import PaymentService
from app.utils.utils import http_exp, logger


class WalletService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session
        self.payment_svc = PaymentService(self.db, self.session)

    async def create_wallet(self, payload: CreateWallet) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create wallet : {payload}")

        try:
            new_wallet = await create_wallet(self.db, payload)
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Wallet record created")

        return APIResponse(data=[map_to_wallet(new_wallet)], traceId=self.session)

    async def get_one_wallet(self, record_id: uuid.UUID) -> APIResponse:
        logger.info(f"{self.session} - Handling request to get wallet using user id : {record_id}")

        payment = await get_wallet_by_id(self.db, record_id)
        if not payment:
            raise http_exp(status_code=404, session=self.session, code="01", exp="No wallet found")

        logger.info(f"{self.session} - Wallet found")

        return APIResponse(data=[map_to_wallet(payment)], traceId=self.session)

    async def list_wallets(self, request: FilterWallet) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering payment(s) using params : {request}")

        wallets, metadata = await filter_wallets(self.db, request)
        wallets_found = True if wallets and len(wallets) > 0 else False

        logger.info(f"{self.session} - Wallet(s) found ? {wallets_found}")
        mapped_wallets = map_to_wallet_list(wallets) if wallets_found else []

        return APIResponseMetadata(data=mapped_wallets, metadata=metadata, traceId=self.session)

    async def credit_wallet(self, payload: CreditWallet):
        logger.info(f"{self.session} - Handling request to credit user wallet : {payload}")

        user_id = payload.user_id
        user_id_uuid = uuid.UUID(user_id)
        amount = payload.amount

        logger.info(f"{self.session} - Getting user details using id : {user_id}")
        from app.user.services.user import UserService
        user_svc = UserService(self.db, self.session)
        user_details = await user_svc.get_one_user(user_id_uuid)
        logger.info(f"{self.session} - User details found. {user_details}")

        payment_request = CreatePayment(amount=amount, user_id=payload.user_id, paymentNonce=payload.payment_nonce)
        logger.info(f"{self.session} - Initiating request to debit user payment method")
        payment_result = await self.payment_svc.initiate_debit(payment_request, user_details.data[0], payload)

        logger.info(f"{self.session} - Payment successful. Crediting wallet using payload : {payload}")
        updated_wallet = await credit_wallet(self.db, user_id_uuid, payload)
        credit_successful = updated_wallet is not None

        logger.info(f"{self.session} - Credit successful ? {credit_successful}")

        if not credit_successful:
            asyncio.create_task(self.__refund_payment_debit(payment_result))
            raise http_exp(status_code=500, session=self.session, code="02", exp="Failed to credit wallet")

        return APIResponse(data=[map_to_wallet(updated_wallet)], traceId=self.session)

    async def debit_wallet(self, user_id: uuid.UUID, amount: float):
        logger.info(f"{self.session} - Debiting {amount} from wallet of user {user_id}")

        updated_wallet = await debit_wallet(self.db, user_id, DebitWallet(amount=amount))
        debit_successful = updated_wallet is not None

        logger.info(f"{self.session} - User debit was successful ? {debit_successful}")

    async def __refund_payment_debit(self, payment_result):
        reference = payment_result.data[0].reference
        external_reference = payment_result.data[0].external_reference

        logger.info(f"{self.session} - Refunding initiated payment debit using {external_reference}")
        await self.payment_svc.refund_debit(external_reference)

        payment_update = UpdatePaymentStatus(status=PaymentStatus.REVERSED)
        logger.info(f"{self.session} - Updating payment status to {payment_update} using reference : {reference}")

        await self.payment_svc.update_payment(reference, payment_update)







