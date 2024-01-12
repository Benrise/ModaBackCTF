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

