from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic
from app.security import hash_password

from datetime import datetime, timedelta, timezone

from app.models.verification import EmailVerification
from app.services.verification import generate_verification_code


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
    expires_at=datetime.now(timezone.utc) + timedelta(minutes=10)
)

    session.add(verification)
    session.commit()

    return user