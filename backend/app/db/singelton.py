from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.core.config import settings

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.engine = create_engine(str(settings.DATABASE_URI))
            cls._instance.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._instance.engine)
        return cls._instance

    def get_session(self):
        return self.SessionLocal()

db = Database()
