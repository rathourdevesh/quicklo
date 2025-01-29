from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
import jwt
# from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

from app.core.constant import UserRoles
from app.core.config import settings
from app.schemas.schemas import TokenData

ALGORITHM = "HS256"


def create_access_token(
        phone_number: int,
        user_name = "",
        user_role: UserRoles = UserRoles.USER.value,
        expires_delta: timedelta = timedelta(minutes=60 * 24 * 7) # 60 minutes * 24 hours * 7 days = 7 days
    ) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "exp": expire,
        "phoneNumber": phone_number,
        "username": user_name,
        "userRole": user_role.value
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_data(token) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        return TokenData(**payload)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
