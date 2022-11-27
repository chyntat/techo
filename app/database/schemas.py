from pydantic import BaseModel
from pydantic import Field, Json
from typing import Dict
from enum import Enum
from app.common.constants import GenderChoices
import datetime


class UserCreate(BaseModel):
    user_id: str | None = None
    email: str
    password: str | None = None
    first_name: str
    last_name: str | None = None
    gender: GenderChoices | None = None
    mobile_number: str
    display_name: str
    location: str | None = None
    about_me: str | None = None
    interests: Json | None = None


class JournalEntryCreate(BaseModel):
    user_id: str
    title: str
    content: str
    tags: Json | None = None
    location: str | None = None
    custom_feelings: Json | None = None


class JournalCommentCreate(BaseModel):
    user_id: str
    journal_id: str
    comment: str
    comment_hash: str
    media_urls: str | None = None
    nsfw_score: float | None = None
    profanity_words: str | None = None
    comment_id: str | None = None


class FollowCreate(BaseModel):
    follower_id: str
    following_id: str


class JournalLikeCreate(BaseModel):
    user_id: str
    journal_id: str
