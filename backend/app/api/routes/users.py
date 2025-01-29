"""user routes."""
from fastapi import APIRouter, Depends

from app.db.conn import get_db_session
from app.schemas.response_schema import build_response
from app.schemas.schemas import AddressData, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.post("/send-otp")
async def send_otp(
    phone_number: int,
    user_service: UserService = Depends(lambda: UserService(session=next(get_db_session())))
):
    """send otp to vendor."""
    status, message = await user_service.send_otp(phone_number)
    return build_response(status=status, data=message, status_code=200 if status else 500)

@router.post("/verify-otp")
async def verify_otp(
    phone_number: int,
    otp: int,
    user_service: UserService = Depends(lambda: UserService(session=next(get_db_session())))
):
    """validate otp and create user."""
    status, message = await user_service.verify_otp(phone_number, otp)
    if not status:
        return build_response(status=status, data=message, status_code=500)
    user = await user_service.get_or_create_user(phone_number)
    return build_response(data=user.phone_number)

@router.post("/address")
async def add_user_address(
    phone_number: int,
    address_data: AddressData,
    user_service: UserService = Depends(lambda: UserService(session=next(get_db_session())))
):
    """add user address."""
    address = await user_service.create_user_address(phone_number, address_data)
    return build_response(data=address.id)

@router.get("")
async def get_user_details(
    phone_number: int,
    user_service: UserService = Depends(lambda: UserService(session=next(get_db_session())))
):
    """add user address."""
    user_data = await user_service.get_user_details(phone_number)
    return UserResponse(
        user_name=user_data.user_name,
        phone_number=user_data.phone_number,
        user_locations=user_data.addresses
    )
