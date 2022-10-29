import logging
from app.routers import users
from app.database.db import init_db, get_session
from app.common.config import Settings
from fastapi import FastAPI

app = FastAPI()

app.include_router(users.router)


@app.on_event("startup")
async def startup():
    if Settings.local_env:
        logging.basicConfig(format='%(asctime)s, %(msecs)d %(lineno)d %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.DEBUG)
    else:
        logging.basicConfig(format='%(asctime)s, %(msecs)d %(lineno)d %(levelname)s - %(message)s',
                            datefmt="%H:%M:%S",
                            level=logging.WARNING)
    await init_db()


logger = logging.getLogger(__name__)
