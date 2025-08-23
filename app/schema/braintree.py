from pydantic import BaseModel


class TransactionOptions(BaseModel):
    submit_for_settlement: bool = True


class Customer(BaseModel):
    id: str
    first_name: str
    last_name: str
    phone: str
    email: str


class Billing(BaseModel):
    first_name: str
    last_name: str
    street_address: str
    locality: str
    region: str
    country_code_alpha2: str


class Shipping(BaseModel):
    first_name: str
    last_name: str
    street_address: str
    locality: str
    region: str
    postal_code: str
    country_code_alpha2: str


class CreateTransaction(BaseModel):
    order_id: str
    amount: str
    customer_id: str
    device_data: str
    payment_method_nonce: str
    billing: Billing
    options: TransactionOptions = TransactionOptions()


class FullTransactionDetails(BaseModel):
    id: str
    type: str
    status: str

    class Config:
        extra = "ignore"


class TransactionResult(BaseModel):
    is_success: bool
    transaction: FullTransactionDetails

    class Config:
        extra = "ignore"


