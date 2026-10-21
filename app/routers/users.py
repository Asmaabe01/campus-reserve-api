
import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.models.verification import EmailVerification
from app.schemas.user import UserCreate, UserPublic
from app.schemas.verification import (
    VerifyEmailRequest,
    ResendCodeRequest,
)
from app.schemas.token import Token
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
)
from app.services.email import send_verification_email
from app.services.verification import generate_verification_code


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


def get_utc_datetime(value: datetime) -> datetime:
    """Normalize SQLite datetimes for UTC comparison."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def create_verification_record(
    user: User,
    session: Session,
) -> str:
    """Invalidate previous codes and create a new code."""

    old_codes = session.exec(
        select(EmailVerification).where(
            EmailVerification.user_id == user.id,
            EmailVerification.is_used == False,
        )
    ).all()

    for old_code in old_codes:
        old_code.is_used = True
        session.add(old_code)

    code = generate_verification_code()

    verification = EmailVerification(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc)
        + timedelta(minutes=10),
    )

    session.add(verification)
    session.commit()

    return code


@router.post("/register", response_model=UserPublic)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session),
):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password),
        is_verified=False,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    code = create_verification_record(user, session)

    try:
        send_verification_email(user.email, code)
    except Exception:
        logger.exception("Failed to send verification email")

        raise HTTPException(
            status_code=503,
            detail=(
                "Could not send the verification email. "
                "Check the server logs."
            ),
        )

    return user


@router.post("/verify-email")
def verify_email(
    data: VerifyEmailRequest,
    session: Session = Depends(get_session),
):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or verification code",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email is already verified",
        )

    verification = session.exec(
        select(EmailVerification)
        .where(
            EmailVerification.user_id == user.id,
            EmailVerification.code == data.code,
            EmailVerification.is_used == False,
        )
        .order_by(EmailVerification.id.desc())
    ).first()

    if not verification:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or verification code",
        )

    expires_at = get_utc_datetime(verification.expires_at)

    if expires_at <= datetime.now(timezone.utc):
        verification.is_used = True
        session.add(verification)
        session.commit()

        raise HTTPException(
            status_code=400,
            detail="Verification code expired. Request a new code.",
        )

    user.is_verified = True
    verification.is_used = True

    session.add(user)
    session.add(verification)
    session.commit()

    return {
        "message": "Email verified successfully",
    }


@router.post("/resend-code")
def resend_code(
    data: ResendCodeRequest,
    session: Session = Depends(get_session),
):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Unable to send a code for this account",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email is already verified",
        )

    code = create_verification_record(user, session)

    try:
        send_verification_email(user.email, code)
    except Exception:
        logger.exception("Failed to resend verification email")

        raise HTTPException(
            status_code=503,
            detail="Could not send the verification email. "
            "Check the server logs.",
        )

    return {
        "message": "If the account can receive a code, "
        "a new verification email has been sent.",
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = session.exec(
        select(User).where(
            User.email == form_data.username
        )
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email before logging in",
        )

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserPublic)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
