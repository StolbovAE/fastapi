import logging
from contextlib import asynccontextmanager

from fastapi import HTTPException, status
import sqlalchemy
import sqlalchemy.exc
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app import config


engine = create_async_engine(config.DATABASE, pool_pre_ping=True)
Base = declarative_base()
async_session = sessionmaker(
	engine, expire_on_commit=False, class_=AsyncSession
)


@asynccontextmanager
async def get_session(self) -> AsyncSession:
	session = self.__async_session()
	try:
		yield session
	except sqlalchemy.exc.IntegrityError as integrity_error:
		await session.rollback()
		logging.warning(integrity_error)
		human_readable_error = await self.__integrity_error_to_human_readable(integrity_error.args[0])
		raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=human_readable_error)
	except Exception as error:
		await session.rollback()
		logging.critical(error)
		raise error
	finally:
		await session.close()
