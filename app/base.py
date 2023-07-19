from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import config


engine = create_async_engine(config.DATABASE, pool_pre_ping=True)
Base = declarative_base()
async_session = sessionmaker(
	engine, expire_on_commit=False, class_=AsyncSession
)
