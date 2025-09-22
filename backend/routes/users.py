from schema.tokenschema import Token
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from os import environ
from schema.userschema import UserExpected, UserResponse
from starlette.status import HTTP_201_CREATED
from typing import Annotated
from uuid import uuid4
from utils.errors import Not_Found, Unauthorized, Forbidden, Bad_Request
from utils.utils import get_user_by_email
from utils.email import send_welcome_email
from utils.security import authenticate_user, create_access_token


load_dotenv()


user_router = APIRouter()


@user_router.post("/register", response_model=UserResponse)
async def register(background_tasks: BackgroundTasks, user_input: UserExpected):
    """Route for Registration"""
    from models.user import User
    from db.reload import storage

    user = get_user_by_email(user_input.email)
    # verify that the user does not exist
    if user:
        raise Bad_Request(detail="Email already registered")

    if not storage.all("User"):
        role = "superuser"
    else:
        role = "user"

    user = User(
        name=user_input.name,
        handle=user_input.handle,
        email=user_input.email,
        password=user_input.password,
        role=role,
        phone_number=user_input.phone_number,
    )
    storage.new(user)
    storage.save()
    background_tasks.add_task(send_welcome_email, user_input.email, user_input.name)
    return JSONResponse(content=user.to_safe_dict(), status_code=HTTP_201_CREATED)


@user_router.post("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise Unauthorized(detail="Incorrect email or Password")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
