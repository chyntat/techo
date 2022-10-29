from app.common.config import get_settings
from app.common.constants import *
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float, Text, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.sql import func
from sqlalchemy.future import select
from app.database.db import Base
from app.common.constants import *

settings = get_settings()


class User(Base):
    """
    This class contains all the fields and relationships of the User model
    """
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True)
    email = Column(String(32), unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    password = Column(String(128), nullable=True)
    first_name = Column(String(32))
    last_name = Column(String(32), nullable=True)
    mobile_number = Column(String(12))
    gender = Column(String, nullable=True)
    user_name = Column(String(32), unique=True, index=True)
    display_name = Column(String(32))
    is_active = Column(Boolean, default=True)
    profile_image = Column(String(128), default=default_profile_url)
    profile_thumbnail = Column(String(128), default=default_profile_url)
    location = Column(String(128), nullable=True)
    last_logged_in = Column(DateTime, server_default=func.now())
    about_me = Column(Text, nullable=True)
    follower_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    interests = Column(JSONB, nullable=True)


class Follower(Base):
    """
    This class contains all the fields and relationships of the Follower model
    """
    __tablename__ = "followers"
    __table_args__ = (
        UniqueConstraint("follower_id", "influencer_id"),
    )
    follower_id = Column(String, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    influencer_id = Column(String, ForeignKey("users.user_id", deferrable=True, initially='DEFERRED'), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    follower = relationship("User", lazy="joined")
    followed = relationship("User", lazy="joined")


class JournalEntry(Base):
    __tablename__ = "journal_entries"
    journal_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id", deferrable=True, initially='DEFERRED'), index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())
    title = Column(String(128))
    content = Column(Text)
    tags = Column(JSONB)
    journal_hash = Column(String(128), index=True)  # for future, to compare hashes for analytics purposes
    media_urls = Column(Text)  # this is a comma separated string of urls
    likes_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    dislikes_count = Column(Integer, default=0)
    bookmarks_count = Column(Integer, default=0)
    reports_count = Column(Integer, default=0)
    custom_feelings = Column(JSONB)
    location = Column(String(128), nullable=True)
    mentions = Column(String)  # TODO: check if this is correct
    nsfw_score = Column(JSONB)
    profanity_words = Column(Text)
    # ^^ list of profane words in the journal entry. these words will be **'d when shared.
    is_sharable = Column(Boolean, default=True)
    # ^^ this will be false if the user violates PII policy or if the user doesn't want to share the journal entry.
    is_approved = Column(Boolean, default=True)
    # ^^ if the journal entry is too profane or nsfw we might want to take an action
    user = relationship("User", lazy='joined')
