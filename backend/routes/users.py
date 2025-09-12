from fastapi import APIRouter
from schema.userschema import UserExpected, UserResponse
from typing import Annotated
from uuid import uuid4
from utils.errors import Not_Found, Unauthorized, Forbidden, Bad_Request

"""from models.user import User"""


user_router = APIRouter()


@user_router.post("/register", response_model=UserResponse)
async def register(user_input: UserExpected):
    """Route for Registration"""
    user = get_user_by_email(user_input.email)
    # verify that the user does not exist
    if user:
        raise Bad_Request(detail="Email already registered")

    return user
