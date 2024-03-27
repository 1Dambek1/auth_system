from fastapi import Cookie, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

from .config import config

from .auth.router_user import app as auth_app
from pathlib import Path

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


# logging
logger.add('logger.log', 
           format='time: {time} / level: "{level}" /  message: "{message}"' ,
           level= "DEBUG",
           rotation="100 MB",
           compression="zip")

# routers



app.include_router(auth_app)




    