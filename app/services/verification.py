
import secrets


def generate_verification_code() -> str:
    """Generate a cryptographically secure six-digit code."""
    return str(secrets.randbelow(900_000) + 100_000)
