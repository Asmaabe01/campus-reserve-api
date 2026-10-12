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
    ResendCodeRequest
)
from app.schemas.token import Token
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)
from app.services.verification import (
    generate_verification_code
)


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/register", response_model=UserPublic)
def register_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hash_password(user_data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    code = generate_verification_code()

    verification = EmailVerification(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc)
        + timedelta(minutes=10)
    )

    session.add(verification)
    session.commit()

    return user


@router.post("/verify-email")
def verify_email(
    data: VerifyEmailRequest,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    verification = session.exec(
        select(EmailVerification).where(
            EmailVerification.user_id == user.id,
            EmailVerification.code == data.code,
            EmailVerification.is_used == False
        )
    ).first()

    if not verification:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification code"
        )

    if verification.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="Verification code expired"
        )

    user.is_verified = True
    verification.is_used = True

    session.add(user)
    session.add(verification)
    session.commit()

    return {
        "message": "Email verified successfully"
    }


@router.post("/resend-code")
def resend_code(
    data: ResendCodeRequest,
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.email == data.email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified"
        )

    code = generate_verification_code()

    verification = EmailVerification(
        user_id=user.id,
        code=code,
        expires_at=datetime.now(timezone.utc)
        + timedelta(minutes=10)
    )

    session.add(verification)
    session.commit()

    return {
        "message": "New verification code generated"
    }


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(
            User.email == form_data.username
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=403,
            detail="Email not verified"
        )

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserPublic)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user