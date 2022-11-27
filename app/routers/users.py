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


@router.post('/update_user', status_code=201)
async def update_user(user: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    user_object = await session.execute(select(models.User).where(models.User.user_id == user.user_id))
    user_object = user_object.scalars().first()
    if user_object:
        user_object.email = user.email
        user_object.mobile_number = user.mobile_number
        user_object.location = user.location
        user_object.about_me = user.about_me
        user_object.interests = user.interests
        user_object.gender = user.gender
        user_object.display_name = user.display_name
        await session.commit()
        return {'status': 'ok', 'user_id': user_object.user_id}
    else:
        return {'status': 'error', 'message': 'User not found'}


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


@router.post('/create_journal_comment', status_code=201)
async def create_journal_comment(journal_comment: schemas.JournalCommentCreate,
                                 session: AsyncSession = Depends(get_session)):
    journal_comment_object = models.JournalComment(**journal_comment.dict())
    journal_comment_object.comment_id = str(uuid.uuid4())
    journal_comment_object.comment_hash = get_hash(journal_comment_object.content)
    journal_comment_object.media_urls = get_urls(journal_comment_object.content)
    journal_comment_object.mentions = get_mentions(journal_comment_object.content)
    journal_comment_object.nsfw_score = get_nsfw_score(journal_comment_object.content)
    journal_comment_object.profanity_words = get_profanity_words(journal_comment_object.content)
    session.add(journal_comment_object)
    await session.commit()
    return {'status': 'ok', 'comment_id': journal_comment_object.comment_id,
            'comment_hash': journal_comment_object.comment_hash}


@router.post('/follow_user', status_code=201)
async def follow_user(follow: schemas.FollowCreate, session: AsyncSession = Depends(get_session)):
    # todo: if already following should be handled from the front end.
    follow_object = models.Follow(**follow.dict())
    follow_object.follow_event_id = str(uuid.uuid4())
    follow_object.follower_id = follow.follower_id
    follow_object.following_id = follow.following_id
    session.add(follow_object)
    await session.commit()
    return {'status': 'ok', 'follow_id': follow_object.follow_event_id}


@router.post('/unfollow_user', status_code=201)
async def unfollow_user(follow: schemas.FollowCreate, session: AsyncSession = Depends(get_session)):
    follow_object = await session.execute(select(models.Follow).filter_by(follower_id=follow.follower_id,
                                                                          following_id=follow.following_id))
    follow_object.status = 'unfollowed'
    await session.commit()
    return {'status': 'ok'}


@router.get('/get_followers/{user_id}', status_code=200)
async def get_followers(user_id: str, session: AsyncSession = Depends(get_session)):
    follow_objects = await session.execute(select(models.Follow).filter_by(following_id=user_id))
    return follow_objects.scalars().all()


@router.get('/get_following/{user_id}', status_code=200)
async def get_following(user_id: str, session: AsyncSession = Depends(get_session)):
    follow_objects = await session.execute(select(models.Follow).filter_by(follower_id=user_id))
    return follow_objects.scalars().all()


@router.post('/create_journal_like', status_code=201)
async def create_journal_like(journal_like: schemas.JournalLikeCreate, session: AsyncSession = Depends(get_session)):
    """
    can be used for both journal like and journal comment like. in the front end for comment like send as journal_id
    """
    journal_like_object = models.JournalLike(**journal_like.dict())
    journal_like_object.like_id = str(uuid.uuid4())
    journal_like_object.user_id = journal_like.user_id
    journal_like_object.journal_id = journal_like.journal_id
    session.add(journal_like_object)
    await session.commit()
    return {'status': 'ok', 'like_id': journal_like_object.like_id}


@router.post('/create_journal_unlike', status_code=201)
async def create_journal_unlike(journal_like: schemas.JournalLikeCreate, session: AsyncSession = Depends(get_session)):
    journal_like_object = await session.execute(select(models.JournalLike).filter_by(user_id=journal_like.user_id,
                                                                                     journal_id=journal_like.journal_id))
    journal_like_object.status = 'unliked'
    await session.commit()
    return {'status': 'ok'}


@router.get('/get_journal_likes/{journal_id}', status_code=200)
async def get_journal_likes(journal_id: str, session: AsyncSession = Depends(get_session)):
    journal_like_objects = await session.execute(select(models.JournalLike).filter_by(journal_id=journal_id))
    return journal_like_objects.scalars().all()
