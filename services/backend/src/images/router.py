from fastapi import APIRouter, Depends
from images.models import image
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from s3 import s3_get_object,list_objects_in_bucket

router = APIRouter()

@router.get("/user/images/{user_id}")
async def get_latest_user_image(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(image.c.file_key).where(image.c.user_id == user_id).order_by(desc(image.c.date_uploaded)).limit(1)
    result = await session.execute(query)
    image_key = result.mappings().first().file_key
    response = s3_get_object(image_key)
    return f'image: {response}'