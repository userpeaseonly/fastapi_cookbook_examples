from enum import Enum

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

class Base(DeclarativeBase):
    pass


class Role(str, Enum):
    basic = "basic"
    premium = "premium"


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    role: Mapped[Role] = mapped_column()
    totp_secret: Mapped[str] = mapped_column(nullable=True)
    role: Mapped[Role] = mapped_column(
        default=Role.basic
    )