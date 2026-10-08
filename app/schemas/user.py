from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    full_name: str
    password: str


class UserPublic(SQLModel):
    id: int
    email: str
    full_name: str
    is_verified: bool