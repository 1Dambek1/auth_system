from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import config

engine = create_async_engine(config.DB_URl)

session = sessionmaker(engine, class_=AsyncSession)


async def get_connection():
    async with session() as connection:
        yield connection


