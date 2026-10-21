
from sqlmodel import SQLModel


class VerifyEmailRequest(SQLModel):
    email: str
    code: str


class ResendCodeRequest(SQLModel):
    email: str
