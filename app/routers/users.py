from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, BackgroundTasks, UploadFile, File
from app.database import models, schemas
from app.database.db import get_session, init_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.common.config import get_settings
from app.core.language_utils import *
from starlette.concurrency import run_in_threadpool
import uuid

settings = get_settings()

router = APIRouter()


@router.post('/create_user', status_code=201)
async def create_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    user_object = models.User(**user.dict())
    user_object.user_id = str(uuid.uuid4())
    user_object.user_name = user_object.display_name.replace(' ', '_') + str(uuid.uuid4())[:4]
    session.add(user_object)
    await session.commit()
    return {'status': 'ok', 'user_id': user_object.user_id}


@router.post('/create_journal_entry', status_code=201)
async def create_journal_entry(journal_entry: schemas.JournalEntryCreate, session: AsyncSession = Depends(get_session)):
    journal_entry_object = models.JournalEntry(**journal_entry.dict())
    journal_entry_object.journal_id = str(uuid.uuid4())
    journal_entry_object.journal_hash = get_hash(journal_entry_object.content)
    journal_entry_object.media_urls = get_urls(journal_entry_object.content)
    journal_entry_object.mentions = get_mentions(journal_entry_object.content)
    journal_entry_object.nsfw_score = get_nsfw_score(journal_entry_object.content)
    journal_entry_object.profanity_words = get_profanity_words(journal_entry_object.content)
    session.add(journal_entry_object)
    await session.commit()
    return {'status': 'ok', 'entry_id': journal_entry_object.journal_id,
            'entry_hash': journal_entry_object.journal_hash}


@router.get('/get_journal_entry/{journal_id}', status_code=200)
async def get_journal_entry(journal_id: str, session: AsyncSession = Depends(get_session)):
    journal_entry_object = await session.execute(select(models.JournalEntry).filter_by(journal_id=journal_id))
    return journal_entry_object.scalars().first()


@router.get('/get_user_journal_entries/{user_id}', status_code=200)
async def get_user_journal_entries(user_id: str, session: AsyncSession = Depends(get_session)):
    journal_entry_objects = await session.execute(select(models.JournalEntry).filter_by(user_id=user_id))
    return journal_entry_objects.scalars().all()


@router.post('/like_journal_entry')
