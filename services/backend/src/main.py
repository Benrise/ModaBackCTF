from datetime import datetime as dt
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from auth.models import User
from auth.schemas import UserOut
from auth.manager import get_user_manager
from config import settings
from s3 import s3_upload

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
]

app = FastAPI(
    title="Moda"
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend]
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

@app.get("/user", response_model=UserOut)
def protected_route(user: User = Depends(current_user)):
    user.registered_at = dt.strftime(user.registered_at, "%m/%d/%Y, %H:%M:%S")
    return user

@app.get("/")
def home():
    return "Hello, CTF Competitor!"

@app.post('/upload')
async def upload(file: UploadFile = None):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No file to upload'
        )
        
    content = await file.read()
    file_size = len(content)
    
    if not 0 < file_size <= 1024*1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Uploaded file is too big. Supported size is 0 - 1 MB'
        )
        
    content_type = file.content_type
        
    if content_type not in settings.SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Unsupported file type. Supported types are JPEG, PNG, and PDF'
        )
        
    uuid = uuid4()
         
    s3_upload(content=content, key=f'{uuid()}.{settings.SUPPORTED_FILE_TYPES[content_type]}')
        
#https://www.youtube.com/watch?v=727l8Asu8P0?t=5:00
#Уязвимость можно создать, если узнавать расширение файла из его названия 