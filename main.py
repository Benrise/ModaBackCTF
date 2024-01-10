from enum import Enum
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Moda"
)

@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )

fake_users = [
    {"id": 1, "role": "admin", "name": "admin"},
    {"id": 2, "role": "user", "name": "Bob"},
    {"id": 3, "role": "user", "name": "Matt"},
    {"id": 4, "role": "user", "name": "Abel", "rights":[
        {"id":1, "created_at": "2020-01-01T00:00:00", "right": "authorization"},
        {"id":2, "created_at": "2020-01-01T00:00:00", "right": "file_uploading"},
        {"id":3, "created_at": "2020-01-01T00:00:00", "right": "chat"}
    ]},
]

class Right(Enum):
    AUTH = "authorization"
    FILE = "file_uploading"
    CHAT = "chat"

class RightsModel(BaseModel):
    id: int
    created_at: datetime
    right: Right

class User(BaseModel):  
    id: int
    role: str
    name: str
    rights: Optional[List[RightsModel]] = None

@app.get("/users/{user_id}", response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]

fake_images = [
    {"id": 1, "user_id":1, "order":1, "image_path":"C:/images/first.png"},
    {"id": 2, "user_id":1, "order":2,"image_path":"C:/images/second.png"},
    {"id": 3, "user_id":1, "order":3, "image_path":"C:/images/third.png"},
]

class Image(BaseModel):
    id: int
    user_id: int
    order: int = Field(ge=0)
    image_path: str

@app.post("/images")
def add_trades(images: List[Image]):
    fake_images.extend(images)
    return {"status": 200, "data": fake_images}
