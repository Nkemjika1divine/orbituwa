from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import environ
from utils.utils import get_user_by_email, get_user_by_handle
import jwt


load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict):
    data_to_encode = data.copy()
    expiry_time = datetime.utcnow() + timedelta(
        hours=int(environ.get("ACCESS_TOKEN_EXPIRY_HOUR"))
    )
    data_to_encode.update({"exp": expiry_time})
    encoded_jwt = jwt.encode(
        data_to_encode,
        environ.get("JWT_SECRET_KEY"),
        algorithm=environ.get("JWT_ALGORITHM"),
    )
    # to get a jwt key, run "openssl rand -hex 32"
    return encoded_jwt


def authenticate_user(email: str, password: str):
    """Authenticates the password of a user. Returns true if the password is correct"""
    from db.reload import storage

    user = get_user_by_email(email)
    if user and user.is_valid_password(password):
        return user
    return False
