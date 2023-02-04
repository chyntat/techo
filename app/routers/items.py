from fastapi import APIRouter, Depends, HTTPException
from app.database import models, schemas

router = APIRouter()


@router.post('/get_comments')
async def get_comments(journal_entry: schemas.JournalEntry):
    pass

