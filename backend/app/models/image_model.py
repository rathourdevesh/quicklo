from sqlalchemy import Column, Integer, LargeBinary, String
from . import Base
from .base_config import BaseConfig


class Images(Base, BaseConfig):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    image_data = Column(LargeBinary)
