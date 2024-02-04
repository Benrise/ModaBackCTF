from datetime import datetime
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend, fastapi_users, current_user
from images.router import router as router_image
from auth.schemas import UserRead, UserCreate
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from database import get_async_session

from auth.models import User
from auth.schemas import UserOut
from auth.manager import get_user_manager
from config import settings
from s3 import s3_upload
from images.utils import create_image_record
from images.schemas import ImageCreate

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

app.include_router(router_image)

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
    user.registered_at = datetime.strftime(user.registered_at, "%m/%d/%Y, %H:%M:%S")
    return user

@app.get("/")
def home():
    return "Hello, CTF Competitor!"

@app.post('/upload')
async def upload(file: UploadFile = None, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
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
        
    image_id = uuid4()
    await create_image_record(
        new_image=ImageCreate(
            user_id=user.id,
            file_key=f'{image_id}.{settings.SUPPORTED_FILE_TYPES[content_type]}',
            content_type=content_type,
            file_size=file_size,
            date_uploaded=datetime.utcnow()
        ),
        session = session
    )
    
    s3_upload(content=content, key=f'{image_id}.{settings.SUPPORTED_FILE_TYPES[content_type]}')
    return {"status": "success"}
        
#https://www.youtube.com/watch?v=727l8Asu8P0?t=5:00
#Уязвимость можно создать, если узнавать расширение файла из его названия