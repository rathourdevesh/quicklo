from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

class BaseConfig:
    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True)
