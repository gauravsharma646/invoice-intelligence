def reconcile_invoice(invoice, payments):

    # Create lookup using invoice number
    payment_map = {
        payment.invoice_number: payment
        for payment in payments
    }

    payment = payment_map.get(
        invoice.invoice_number
    )

    # Payment does not exist
    if payment is None:
        return {
            "status": "MISSING_PAYMENT",
            "message": "No payment found"
        }

    # Check vendor
    if invoice.vendor_name.lower() != payment.vendor_name.lower():
        return {
            "status": "VENDOR_MISMATCH",
            "message": "Vendor does not match"
        }

    # Check amount
    if abs(invoice.amount - payment.amount) > 0.01:
        return {
            "status": "AMOUNT_MISMATCH",
            "message": (
                f"Invoice amount: {invoice.amount}, "
                f"Payment amount: {payment.amount}"
            )
        }

    return {
        "status": "MATCHED",
        "message": "Invoice successfully reconciled"
    }