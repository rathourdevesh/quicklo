from typing import Generator
from app.db.singelton import db
from sqlalchemy.orm import Session

def get_db_session() -> Generator[Session, None, None]:
    session = db.get_session()
    try:
        yield session
    finally:
        session.close()
