from fastapi import APIRouter
from pydantic import BaseModel
import smtplib

import os
from email.mime.text import MIMEText

router = APIRouter(prefix="/email", tags=["Email"])


class EmailRequest(BaseModel):
    email: str
    username: str


def send_email(to_email: str, username: str):

    # ✅ Get credentials from .env
    sender_email = os.getenv("EMAIL_USER")
    app_password = os.getenv("EMAIL_PASSWORD")

    subject = "Activate your CtrlS account 🚀"

    try:
        with open("app/templates/email_template.html", "r", encoding="utf-8") as file:
            html_template = file.read()
    except Exception as e:
        print("Template load error:", e)
        return

    # ✅ Replace template variables
    body = html_template.replace("{{ name }}", username)
    body = body.replace("{{ admin_email }}", to_email)
    body = body.replace("{{ organization }}", "CtrlS")
    body = body.replace("{{ plan }}", "Free Plan")

    # ✅ Create HTML email
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            print("EMAIL_USER:", sender_email)
            print("EMAIL_PASSWORD:", app_password)
            server.login(sender_email, app_password)
            server.send_message(msg)
            print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", e)


@router.post("/send-email")
def send_email_api(data: EmailRequest):

    send_email(data.email, data.username)

    return {
        "message": "Email sent successfully ✅"
    }