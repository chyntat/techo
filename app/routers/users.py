from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, BackgroundTasks, UploadFile, File
from app.database import models, schemas
from app.database.db import get_session, init_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.common.config import get_settings
from starlette.concurrency import run_in_threadpool
import uuid

settings = get_settings()

router = APIRouter()


@router.post('/create_user', status_code=201)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    user_object = models.User(**user.dict())
    user_object.user_id = uuid.uuid4()
    user_object.user_name = user_object.display_name.replace(' ', '_') + str(uuid.uuid4()[:4])
    session.add(user_object)
    await session.commit()
    return
