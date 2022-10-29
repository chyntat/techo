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
