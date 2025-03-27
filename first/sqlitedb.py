from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import Base


DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        print("Opening db connection")
        yield db
    finally:
        print("Closing db connection")
        db.close()
