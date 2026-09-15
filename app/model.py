from sqlalchemy import Column, Integer, String, Float, Date

from .database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String, unique=True, index=True)
    vendor_name = Column(String, index=True)

    invoice_date = Column(Date)

    amount = Column(Float)
    tax = Column(Float)

    status = Column(
        String,
        default="PENDING"
    )


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    transaction_id = Column(
        String,
        unique=True,
        index=True
    )

    invoice_number = Column(String, index=True)

    vendor_name = Column(String)

    payment_date = Column(Date)

    amount = Column(Float)

    status = Column(
        String,
        default="UNMATCHED"
    )