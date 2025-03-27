from email_validator import (
    EmailNotValidError,
    validate_email,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import Role, User

pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)


def add_user(
    session: Session,
    username: str,
    email: str,
    password: str,
    role: Role = Role.basic,
) -> User | None:
    hashed_password = pwd_context.hash(password)
    print("Hashed Password: ", hashed_password)
    print("Role: ", role)
    print("Username: ", username)
    print("Email: ", email)
    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role,
    )
    print(db_user)
    session.add(db_user)
    try:
        print("DB User attributesss:", db_user.__dict__)
        session.commit()
        session.refresh(db_user)
    except IntegrityError as e:
        print("Error: ", e)
        session.rollback()
        return
    print("DB User: ", db_user)
    return db_user


def get_user(
    session: Session, username_or_email: str
) -> User | None:
    try:
        validate_email(username_or_email)
        query_filter = User.email
    except EmailNotValidError:
        query_filter = User.username
    user = (
        session.query(User)
        .filter(query_filter == username_or_email)
        .first()
    )
    return user