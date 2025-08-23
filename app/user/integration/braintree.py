import braintree

from app.schema.braintree import CreateTransaction, TransactionResult, FullTransactionDetails, Customer
from app.settings import settings
from app.utils.utils import http_exp, logger


def get_braintree_env_equivalent(env: str):
    env_records = {
        "sandbox": braintree.Environment.Sandbox,
        "production": braintree.Environment.Production
    }
    return env_records.get(env)


gateway = braintree.BraintreeGateway(
  braintree.Configuration(
      environment=get_braintree_env_equivalent(settings.BRAINTREE_ENV),
      merchant_id=settings.BRAINTREE_MERCHANT_ID,
      public_key=settings.BRAINTREE_PUBLIC_KEY,
      private_key=settings.BRAINTREE_PRIVATE_KEY
  )
)


async def create_customer(session: str, customer: Customer):
    logger.info(f"{session} - Creating braintree customer : {customer}")

    result = gateway.customer.create(customer.model_dump())
    customer_created = result is not None and result.is_success

    if not customer_created:
        logger.error(f"{session} - Failed to create braintree customer")

    logger.info(f"{session} - New braintree customer created")


async def generate_client_token(session: str, customer_id: str):
    logger.info(f"{session} - Generating token for customer : {customer_id}")

    client_token = gateway.client_token.generate({
        "customer_id": customer_id
    })

    token_generated = client_token is not None
    logger.info(f"{session} - Token generated ? {token_generated}")

    if not token_generated:
        raise http_exp(500, session=session, exp="Failed to generate token")

    return client_token


async def initiate_payment(session: str, request: CreateTransaction) -> TransactionResult:
    logger.info(f"{session} - Calling braintree to process new payment request : {request}")

    payment_result = gateway.transaction.sale(request.model_dump())
    payment_successful = payment_result.is_success

    logger.info(f"{session} - Payment successful ? {payment_successful}")

    if not payment_successful:
        raise http_exp(500, session=session, exp="Payment failed")

    vendor_transaction = payment_result.transaction
    transaction_details = TransactionResult(
        is_success=payment_successful,
        transaction=FullTransactionDetails(
            id=vendor_transaction.id,
            type=vendor_transaction.type,
            status=vendor_transaction.status
        )
    )

    return transaction_details


async def initiate_reversal(session: str, transaction_id: str):
    logger.info(f"{session} - Calling braintree to reverse transaction using id : {transaction_id}")

    reversal_result = gateway.transaction.refund(transaction_id)
    reversal_successful = reversal_result.is_success

    logger.info(f"{session} - Payment reversed ? {reversal_successful}")

    if not reversal_successful:
        raise http_exp(500, session=session, exp="Reversal failed")

