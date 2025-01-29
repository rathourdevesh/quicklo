"""Users Service."""

from sqlalchemy.orm import joinedload

from app.models.user_model import UserAddress
from app.schemas.schemas import AddressData
from .base_service import BaseService
from app.models import Users
from app.core.logger_config import logger
from app.core.security import create_access_token

class UserService(BaseService):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def send_otp(self, phone_number: int) -> tuple[bool, str]:
        """Call client to send otp."""
        logger.info(f"send otp for {phone_number}")
        return True, "OTP sent successfully"

    async def verify_otp(self, phone_number: int, otp: int) -> tuple[bool, str]:
        """Call client to verify otp."""
        logger.info(f"verify otp for {phone_number} :: {otp}")
        return True, "OTP verified"

    async def get_user(self, phone_number: int) -> Users:
        """get user against phone_number."""
        return self.session.query(Users).filter(phone_number == phone_number).first()

    async def get_or_create_user(self, phone_number: int) -> Users:
        """Create user against phone_number if not exists."""
        user = self.get_user(phone_number)
        if user:
            return user
        user = Users(
            token=create_access_token(phone_number),
            phone_number=phone_number,
        )
        self.session.add(user)
        self.session.commit()
        return user

    async def create_user_address(self, phone_number: int, address_data: AddressData) -> Users:
        """add address for phone_number."""
        user = self.get_user(phone_number)
        if not user:
            raise ValueError("User with this mobile number does not exist")
        address = UserAddress(user_id=user.id, **address_data.__dict__)
        self.session.add(address)
        self.session.commit()
        return address

    async def get_user_details(self, phone_number: int) -> Users:
        """Get user details along with its address,"""
        user = (
            self.session.query(Users)
            .options(joinedload(Users.addresses))
            .filter(Users.phone_number == phone_number)
            .first()
        )
        return user
