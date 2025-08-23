import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.schema.braintree import CreateTransaction, Billing
from app.schema.user import GetUser
from app.schema.enums import PaymentStatus
from app.schema.wallet import CreditWallet
from app.user.exceptions.custom_exceptions import DatabaseException
from app.user.integration.braintree import generate_client_token, initiate_payment, initiate_reversal
from app.utils.mappers import map_to_payment, map_to_payment_list
from app.user.models import Payment
from app.user.repo.payment import create_payment, update_payment_by_reference, get_payment_by_reference, filter_payment
from app.schema.payment import CreatePayment, UpdatePaymentStatus, FilterPayment, GenerateTokenAPIResponse, \
    APIResponse, APIResponseMetadata
from app.settings import settings
from app.utils.utils import http_exp, logger


class PaymentService:
    def __init__(self, db: AsyncSession, session: str):
        self.db = db
        self.session = session

    async def generate_client_token(self, customer_id: uuid.UUID) -> GenerateTokenAPIResponse:
        logger.info(f"{self.session} - Handle generate payment token request for user : {customer_id}")

        from app.user.services.user import UserService
        user_svc = UserService(self.db, self.session)

        await user_svc.get_one_user(customer_id)
        logger.info(f"{self.session} - User record found")

        token = await generate_client_token(self.session, str(customer_id))

        logger.info(f"{self.session} - Customer token generated")

        return GenerateTokenAPIResponse(data=[token], traceId=self.session)

    async def initiate_debit(
        self,
        payload: CreatePayment,
        user: GetUser,
        customer_payment: CreditWallet
    ) -> APIResponse:
        logger.info(f"{self.session} - Handling request to create payment for customer {user.id.value} : {payload}")

        try:
            new_payment = await create_payment(self.db, payload)
            reference = new_payment.reference
        except DatabaseException as exp:
            raise http_exp(status_code=500, session=self.session, exp=str(exp))
        except Exception as exp:
            raise http_exp(500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Payment record created")

        transaction_payload = await build_transaction_payload(user, reference, customer_payment)
        logger.info(f"{self.session} - Initiating debit on customer payment method")

        try:
            payment_result = await initiate_payment(self.session, transaction_payload)
        except Exception as exp:
            logger.error(f"{self.session} - {str(exp)}. Payment failed. Updating payment status to failed", exc_info=True)
            await self.update_payment(reference, UpdatePaymentStatus(status=PaymentStatus.FAILED))
            raise http_exp(status_code=500, session=self.session, exp=str(exp))

        logger.info(f"{self.session} - Updating payment successful")
        external_reference = payment_result.transaction.id
        payment_update = UpdatePaymentStatus(status=PaymentStatus.SUCCESSFUL, externalReference=external_reference)
        updated_payment = await self.update_payment(reference, payment_update)

        return APIResponse(data=[map_to_payment(updated_payment)], traceId=self.session)

    async def refund_debit(self, transaction_id):
        logger.info(f"{self.session} - Refunding payment debit using external transaction id : {transaction_id}")
        await initiate_reversal(self.session, transaction_id)

        logger.info(f"{self.session} - Refund completed")

    async def get_one_payment(self, payment_id: uuid.UUID):
        logger.info(f"{self.session} - Handling request to get payment using id : {payment_id}")

        payment = await get_payment_by_reference(self.db, payment_id)
        if not payment:
            raise http_exp(status_code=404, session=self.session, code="01", exp="No payment found")

        logger.info(f"{self.session} - Payment found")
        result_map = map_to_payment(payment)

        return APIResponse(data=[result_map], traceId=self.session)

    async def list_payments(self, request: FilterPayment) -> APIResponseMetadata:
        logger.info(f"{self.session} - Filtering payment(s) using params : {request}")

        payments, metadata = await filter_payment(self.db, request)
        payments_found = True if payments and len(payments) > 0 else False

        logger.info(f"{self.session} - Payment(s) found ? {payments_found}")
        mapped_payments = map_to_payment_list(payments) if payments_found else []

        return APIResponseMetadata(data=mapped_payments, metadata=metadata, traceId=self.session)

    async def update_payment(self, reference: uuid.UUID, update_payload: UpdatePaymentStatus) -> Payment:
        update_result = await update_payment_by_reference(self.db, record_id=reference, payload=update_payload)
        payment_updated = update_result is not None

        if not payment_updated:
            raise http_exp(status_code=500, session=self.session, exp="Unexpected error occurred")

        logger.error(f"{self.session} - Payment updated ? {payment_updated}")

        return update_result


async def build_transaction_payload(
    user: GetUser,
    reference: uuid.UUID,
    customer_payment: CreditWallet
) -> CreateTransaction:
    location = user.location
    street = location.street

    billing = Billing(
        first_name=user.name.first,
        last_name=user.name.last,
        street_address=f"{street.name} {street.number}",
        locality=location.city,
        region=location.state,
        country_code_alpha2=location.country
    )

    transaction_request = CreateTransaction(
        amount=str(customer_payment.amount),
        order_id=str(reference),
        payment_method_nonce=customer_payment.payment_nonce,
        device_data=customer_payment.device_data.correlation_id,
        customer_id=user.id.value,
        billing=billing
    )

    return transaction_request


