from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Invoice, Payment
from .schemas import InvoiceCreate, PaymentCreate
from .reconciliation import reconcile_invoice


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Invoice Intelligence & Reconciliation API"
)


@app.get("/")
def home():
    return {
        "message": "Invoice Intelligence API is running"
    }


@app.post("/invoices")
def create_invoice(
    invoice: InvoiceCreate,
    db: Session = Depends(get_db)
):
    new_invoice = Invoice(
        invoice_number=invoice.invoice_number,
        vendor_name=invoice.vendor_name,
        invoice_date=invoice.invoice_date,
        amount=invoice.amount,
        tax=invoice.tax
    )

    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)

    return new_invoice


@app.post("/payments")
def create_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    new_payment = Payment(
        transaction_id=payment.transaction_id,
        invoice_number=payment.invoice_number,
        vendor_name=payment.vendor_name,
        payment_date=payment.payment_date,
        amount=payment.amount
    )

    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    return new_payment


@app.get("/reconcile/{invoice_number}")
def reconcile(
    invoice_number: str,
    db: Session = Depends(get_db)
):
    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_number == invoice_number
        )
        .first()
    )

    if not invoice:
        return {
            "error": "Invoice not found"
        }

    payments = db.query(Payment).all()

    result = reconcile_invoice(
        invoice,
        payments
    )

    invoice.status = result["status"]

    db.commit()

    return {
        "invoice_number": invoice_number,
        "result": result
    }