from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.database import models, schemas

router = APIRouter()
templates = Jinja2Templates(directory="app/static/templates")


@router.get('/home', status_code=200)
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
