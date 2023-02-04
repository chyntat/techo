import logging

from starlette.staticfiles import StaticFiles

from app.routers import users, landing
from app.database.db import init_db, get_session
from app.common.config import get_settings
from fastapi import FastAPI

app = FastAPI()
settings = get_settings()
app.mount("/static", StaticFiles(directory="app/static/"), name="static")
app.include_router(users.router)
app.include_router(landing.router)


@app.on_event("startup")
async def startup():
    if settings.local_env:
        logging.basicConfig(format='%(asctime)s, %(msecs)d %(lineno)d %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s, %(msecs)d %(lineno)d %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.WARNING)
    await init_db()


logger = logging.getLogger(__name__)
