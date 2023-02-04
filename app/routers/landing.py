from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import models, schemas
from app.common.config import get_settings
from app.routers.users import get_journal_entries_landing
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session

router = APIRouter()
settings = get_settings()
templates = Jinja2Templates(directory="app/static/templates")


@router.get('/home', status_code=200)
async def get_index(request: Request, session: AsyncSession = Depends(get_session)):
    joi_logo = settings.base_url + '/static/assets/images/joi_logo.png'
    print(joi_logo)
    resp = await get_journal_entries_landing(user_id='51dee06e-41e7-47d7-940e-4ab1dee571a8', session=session)
    print()
    print(resp['today'])
    print(resp['yesterday'])
    return templates.TemplateResponse("index.html", {"request": request, 'joi_logo': joi_logo, 'today': resp['today']['post'], 'today_date': resp['today']['date'], 'yesterday': resp['yesterday']['post'], 'yesterday_date': resp['yesterday']['date']})
