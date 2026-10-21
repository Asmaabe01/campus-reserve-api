
import os
from pathlib import Path

import resend
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def send_verification_email(to_email: str, code: str) -> None:
    """Send an account verification code through Resend."""

    api_key = os.getenv("RESEND_API_KEY")
    email_from = os.getenv(
        "EMAIL_FROM",
        "onboarding@resend.dev",
    )

    if not api_key:
        raise RuntimeError(
            "RESEND_API_KEY is missing from the .env file"
        )

    resend.api_key = api_key

    params = {
        "from": email_from,
        "to": [to_email],
        "subject": "Verify your CampusReserve account",
        "text": (
            "Hello,\n\n"
            f"Your CampusReserve verification code is: {code}\n\n"
            "This code expires in 10 minutes and can only be "
            "used once.\n\n"
            "If you did not request this code, you can ignore "
            "this email.\n\n"
            "CampusReserve Team"
        ),
    }

    resend.Emails.send(params)
