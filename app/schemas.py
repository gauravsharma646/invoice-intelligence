from datetime import date

from pydantic import BaseModel


class InvoiceCreate(BaseModel):
    invoice_number: str
    vendor_name: str
    invoice_date: date
    amount: float
    tax: float


class PaymentCreate(BaseModel):
    transaction_id: str
    invoice_number: str
    vendor_name: str
    payment_date: date
    amount: float