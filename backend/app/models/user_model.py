from sqlalchemy import BigInteger, Column, Enum, ForeignKey, Float, Integer, String, UniqueConstraint
from sqlalchemy.orm import validates, relationship

from . import Base
from .base_config import BaseConfig
from app.core.constant import UserRoles

class Users(Base, BaseConfig):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    phone_number = Column(BigInteger, unique=True, nullable=False)
    token = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    role = Column(Enum(UserRoles), default=UserRoles.USER, nullable=False)

    __table_args__ = (
        UniqueConstraint('phone_number', name='uq_users_phone_number'),
    )

    @validates("phone_number")
    def validate_phone_number(self, _, value):
        if len(str(value)) != 10:
            raise ValueError("Mobile number must be exactly 10 digits.")
        return value

class UserAddress(Base, BaseConfig):
    __tablename__ = "user_address"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    userid = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    country_code = Column(String(5), nullable=False)
    state_code = Column(String(5), nullable=False)
    city_code = Column(String(20), nullable=False)
    pincode = Column(Integer, nullable=False)
    address1 = Column(String, nullable=False)
    address2 = Column(String, nullable=True)
    landmark = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    store_loaction_id = Column(Integer, nullable=False)

    user = relationship("User", back_populates="addresses")
