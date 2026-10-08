from sqlmodel import SQLModel


class VerifyEmailRequest(SQLModel):
    email: str
    code: str