from collections import UserDict
from enum import Enum
from fastapi import Depends, FastAPI
from typing import Annotated, List, Optional, Union
import fastapi_users
from pydantic import BaseModel, Field
from datetime import datetime

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from auth.auth import auth_backend
from auth.database import User
from auth.schemas import UserRead, UserCreate
from auth.user_manager import get_user_manager

app = FastAPI(
    title="Moda"
)

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )
    
fastapi_users = fastapi_users.FastAPIUsers[UserDict, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, guest!"
