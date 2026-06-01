"""
Invoice PDF service.
"""

import os

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class InvoiceService:
    """Invoice PDF generator."""

    def generate_invoice(
        self,
        invoice_number: str,
        amount,
        payment_date,
        vendor: str
    ):

        os.makedirs(
            "invoices",
            exist_ok=True
        )

        file_path = (
            f"invoices/{invoice_number}.pdf"
        )

        pdf = canvas.Canvas(
            file_path,
            pagesize=letter
        )

        pdf.drawString(
            100,
            750,
            "AI FinOps Platform"
        )

        pdf.drawString(
            100,
            720,
            f"Invoice Number: {invoice_number}"
        )

        pdf.drawString(
            100,
            700,
            f"Vendor: {vendor}"
        )

        pdf.drawString(
            100,
            680,
            f"Amount: {amount}"
        )

        pdf.drawString(
            100,
            660,
            f"Payment Date: {payment_date}"
        )

        pdf.save()

        return file_path


invoice_service = (
    InvoiceService()
)