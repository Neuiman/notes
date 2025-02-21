from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import Settings

engine = create_async_engine(Settings.ASYNC_DB_URL, future=True, echo=True)

session_maker = async_sessionmaker(engine, expire_on_commit=False)

def connection(method):

    async def wrapper(*args, **kwargs):

        async with session_maker() as session:

            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper

