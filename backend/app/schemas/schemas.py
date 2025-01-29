from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from app.core.constant import UserRoles

class TokenData(BaseModel):
    username: str
    phoneNumber: int
    userRole: UserRoles

class AddressBase(BaseModel):
    country_code: str
    state_code: str
    city_code: str
    pincode: Optional[int]
    address1: str
    address2: Optional[str]
    landmark: Optional[str]

class AddressData(AddressBase):
    latitude: float
    longitude: float

class UserAddressResponse(AddressBase):
    store_location_id: int

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user_name: Optional[str]
    phone_number: int
    user_locations: list[UserAddressResponse]

    class Config:
        orm_mode = True
